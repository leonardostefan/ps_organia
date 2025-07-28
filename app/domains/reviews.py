from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import pandas as pd
from pysentimiento import create_analyzer
from typing import List
import database.review as review_crud


class ReviewDomain:
    analyzer = create_analyzer(task="sentiment", lang="pt")

    async def create_review(
        self,
        review: object,
        session: Session,
    ) -> dict:
        """
        Processamento e armazenamento de uma avaliação.
        Recebe os dados da avaliação, faz a chamada da avaliação de sentimento e realiza a persistencia no banco de dados

        Parameters
        ---------
        review: object
            Objeto de uma review
        session: Session
            Sessão para conexão com o BD

        Returns
        ---------
        dict
            Dicionario com os dados da review persistida
        """

        review_dict: dict = review.dict()

        sentiment = self._evaluate_text_sentiment(review_dict)
        review_dict.update(
            {
                "sentiment": sentiment,
                "created_at": datetime.now(),
            }
        )
        result = review_crud.create(session, review_dict)
        return result.to_response()

    async def get_reviews(
        self,
        session: Session,
        start_date: str,
        end_date: str,
    )->List[dict]:
        """
        Busca de avaliações no range de datas infomado.
        Busca de avaliações no range de datas infomado, se não houver data informada busca desde o inicio e fim das avaliações.

        Parameters
        ---------
        session: Session
            Sessão para conexão com o BD
        start_date: str
            Data mais antiga para o range da busca
        end_date: str
            Data mais recente para o range da busca, data final.

        Returns
        ---------
        dict
            Lista de dicionarios contendo as reviews do periodo
        """
        query_result = await review_crud.read_by_date_range(
            session,
            start_date=start_date,
            end_date=end_date,
        )

        reviews = [r.to_response() for r in query_result]

        return reviews

    async def get_review_by_id(
        self,
        id: int,
        session: Session,
    ) -> dict:
        """
        Busca de uma unica avaliação a partir do seu `id`.

        Parameters
        ---------
        id:int
            Id da review desejada
        session: Session
            Sessão para conexão com o BD
        Returns
        ---------
        dict
            Dicionario contendo a review indicada

        Raises:
        --------
        HTTPException
            exceção http com status 404 caso não encontre o review com a id informada
        """

        review = await review_crud.read_one(session, id=id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review.to_response()

    async def get_report(
        self,
        start_date: str,
        end_date: str,
        session: Session,
    ) -> dict:
        """
        Report do sentimento das avaliações do periodo
        Busca de avaliações no range de datas infomado e calcula a quantidade distinta de cada avaliação "positiva"/"negativa"/"neutra".
        Se não houver data informada busca desde o inicio e fim das avaliações.


        Parameters
        ---------
        start_date: str
            Data mais antiga para o range da busca
        end_date: str
            Data mais recente para o range da busca, data final.

        session: Session
            Sessão para conexão com o BD
        Returns
        ---------
        dict
            Dicionario contendo a contagem dos sentimentos
            (Ex: `{"positiva": 13,"negativa": 6,"neutra": 3}`)

        """
        # Busca no BD
        query_result = await review_crud.read_by_date_range(
            session, start_date=start_date, end_date=end_date
        )

        # Processa dados buscados
        result_df = pd.DataFrame([r.to_response() for r in query_result])

        return result_df["sentiment"].value_counts().to_dict()

    def _evaluate_text_sentiment(self, review: dict) -> str:
        """
        Método para fazer a predição do texto de uma avaliação


        Parameters
        ---------
        review:dict
            Dicionario com os dados da review (só é necessário a chave `"text"`)

        Returns
        ---------
        str
            "positiva"/"negativa"/"neutra"
        """

        result = self.analyzer.predict(review["text"])

        label_map = {"POS": "positiva", "NEG": "negativa", "NEU": "neutra"}

        return label_map.get(result.output)

    async def test_evaluation(self, session) -> dict:
        """
        Metodo para validação do modelo de analise de sentimento.
        Busca todas avaliações ja feitas e as analise de sentimento registradas no passado e realiza uma nova analise de sentimento. Todos resultados que divergirem serão retornados


        Parameters
        ---------
        session: Session
            Sessão para conexão com o BD

        Returns
        ---------
        dict
            "count":int
                contagem de itens que divergem
            "diff_list":list
                Lista com os dicionarios das informações das reviews que deram divergencia no predict novo com o antigo.
        """
        query_result = await review_crud.read_by_date_range(
            session, start_date="", end_date=""
        )

        def compare_evaluate(db_review)->dict:
            dict_review: dict = db_review.to_response()
            dict_review.update(
                {
                    "new_model_eval": self._evaluate_text_sentiment(dict_review),
                }
            )
            return dict_review

        test_result = [compare_evaluate(q) for q in query_result]

        diff_list = []
        for r in test_result:
            if r["sentiment"] != r["new_model_eval"]:
                diff_list.append(r)

        return {
            "count": len(diff_list),
            "diff_list": diff_list,
        }

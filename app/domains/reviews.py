from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import pandas as pd
from pysentimiento import create_analyzer

import database.review as review_crud


class ReviewDomain:
    analyzer = create_analyzer(task="sentiment", lang="pt")

    async def create_review(
        self,
        review: object,
        session: Session,
    ):
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
    ):
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
    ):
        review = await review_crud.read_one(session, id=id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    async def get_report(
        self,
        start_date: str,
        end_date: str,
        session: Session,
    ):
        # Busca no BD
        query_result = await review_crud.read_by_date_range(
            session, start_date=start_date, end_date=end_date
        )

        # Processa dados buscados
        result_df = pd.DataFrame([r.to_response() for r in query_result])

        return result_df["sentiment"].value_counts().to_dict()

    def _evaluate_text_sentiment(self, review: dict):
        """
        Chamada do avaliador de sentimento do texto
        """

        result = self.analyzer.predict(review["text"])

        label_map = {"POS": "positiva", "NEG": "negativa", "NEU": "neutra"}

        return label_map.get(result.output)

    async def test_evaluation(self, session):
        query_result = await review_crud.read_by_date_range(
            session, start_date="", end_date=""
        )

        def compare_evaluate(db_review):
            dict_review = db_review.to_response()
            dict_review.update(
                {
                    "model_eval": self._evaluate_text_sentiment(dict_review),
                }
            )
            return dict_review

        test_result = [compare_evaluate(q) for q in query_result]

        diff_list = []
        for r in test_result:
            if r["sentiment"] != r["model_eval"]:
                diff_list.append(r)

        return {
            "count": len(diff_list),
            "diff_list": diff_list,
        }

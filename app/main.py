from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from typing import Annotated
from fastapi.responses import RedirectResponse

from database.models import Review
from database.con import get_session
from schemas import Review, ReviewCreate
from domains.reviews import ReviewDomain

app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# Definição das rotas
@app.post("/reviews/", response_model=Review)
async def create_review(
    review: ReviewCreate,
    session: SessionDep,
):
    """
    Insere uma nova revisão no banco de dados, realizando a inferencia do sentimento da mensagem.
    """
    domain = ReviewDomain()

    return await domain.create_review(session=session, review=review)


### OK -----
@app.get("/reviews/", response_model=List[Review])
async def get_reviews(
    session: SessionDep,
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    """
    Retorna uma lista de avaliações analisadas,juntamente com suas respectivas classificações. Permite filtrar os resultados por intervalo de datas, conforme a necessidade.
    """
    domain = ReviewDomain()
    reviews = await domain.get_reviews(
        session=session,
        start_date=start_date,
        end_date=end_date,
    )

    return reviews


### OK -----
@app.get("/reviews/{id}", response_model=Review)
async def get_review(
    id: int,
    session: SessionDep,
):
    """
    Busca a análise de um comentário específico pelo ID do mesmo
    """
    domain = ReviewDomain()
    review = await domain.get_review_by_id(
        id=id,
        session=session,
    )
    return review


@app.get("/reviews/report/", response_model=dict)
async def get_report(
    start_date: str,
    end_date: str,
    session: SessionDep,
):
    """
    Retorna um relatório das avaliações realizadas em um determinado período, incluindo a contagem das avaliações classificadas como positiva, negativa ou neutra.
    """

    domain = ReviewDomain()
    report = await domain.get_report(
        start_date=start_date,
        end_date=end_date,
        session=session,
    )
    return report


@app.get("/reviews/eval_model/", response_model=dict)
async def get_test_evaluation(
    session: SessionDep,
):
    """
    Faz uma avaliação global de todos os valores já salvos no banco de dados e compara se o modelo de Analise de sentimentos atual com o que ja foi inferido anteriormente.
    """

    domain = ReviewDomain()
    report = await domain.test_evaluation(
        session=session,
    )
    return report


### Redirencionamento para swagger:


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/swagger", include_in_schema=False)
def swagger():
    return RedirectResponse(url="/docs")

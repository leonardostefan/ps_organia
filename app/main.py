from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from typing import Annotated

from database.models import Review

from database.con import get_session,
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
    domain = ReviewDomain()

    return await domain.create_review(session=session, review=review)


### OK -----
@app.get("/reviews/", response_model=List[Review])
async def get_reviews(
    session: SessionDep,
    start_date: str = Query(None),
    end_date: str = Query(None),
):
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
    domain = ReviewDomain()
    report = await domain.get_report(
        start_date=start_date,
        end_date=end_date,
        session=session,
    )
    return report

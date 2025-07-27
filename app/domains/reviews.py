from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import pandas as pd

import database.review as review_crud


class ReviewDomain:

    async def create_review(
        self,
        review: object,
        session: Session,
    ):
        review_dict: dict = review.dict()
        review_dict.update(
            {
                "sentiment": "positiva",
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

from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
from database.models import Review
import json


def custom_serializer(o):
    if isinstance(o, date):
        return str(o.isoformat())
    raise TypeError(f"Tipo não serializável: {type(o)}")


def create(db: Session, obj_in):
    db_obj = Review(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


async def read_by_date_range(
    db: Session, start_date: str = None, end_date: str = None
) -> List[Review]:
    query = db.query(Review)

    if start_date:
        query = query.filter(Review.created_at >= start_date)
    if end_date:
        query = query.filter(Review.created_at <= end_date)

    return_list = [r.to_response() for r in query.all()]

    return return_list


### OK -----
async def read_one(db: Session, id: int) -> Review:
    result = db.query(Review).filter(Review.id == id).first()
    return result.to_response()


async def generate_report(db: Session, start_date: str, end_date: str):
    import pandas as pd

    start_date: date = (
        date(datetime.strptime(start_date, "%d/%m/%y")) if start_date != "" else None
    )
    end_date: date = (
        date(datetime.strptime(end_date, "%d/%m/%y")) if end_date != "" else None
    )

    query = (Review.created_at >= start_date if start_date else True) & (
        Review.created_at <= end_date if end_date else True
    )

    query_result = db.query(Review).filter(query).all()
    result_df = pd.DataFrame([r.to_response() for r in query_result])
    return result_df["sentiment"].value_counts().to_dict()

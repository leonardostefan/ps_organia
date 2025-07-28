from typing import List

from database.models import Review
from sqlalchemy.orm import Session


def create(db: Session, review_dict: dict):
    db_obj = Review(**review_dict)
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

    return query.all()


### OK -----
async def read_one(db: Session, id: int) -> Review:
    result = db.query(Review).filter(Review.id == id).first()
    return result

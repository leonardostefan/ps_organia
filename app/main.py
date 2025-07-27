
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from typing import Annotated

from database.models import Review
import database.crud as review_crud
from database.con import get_session
from schemas import Review

app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]



### OK -----
@app.get("/reviews/", response_model=List[Review])
async def get_reviews(
    session: SessionDep,
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    reviews = await review_crud.read_by_date_range(
        session, start_date=start_date, end_date=end_date
    )
    return reviews

### OK -----
@app.get("/reviews/{id}", response_model=Review)
async def get_review(
    id: int,
    session: SessionDep,
):
    review = await review_crud.read_one(session, id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@app.get("/reviews/report/", response_model=dict)
async def get_report(
    start_date: str,
    end_date: str,
    session: SessionDep,
):
    report = await review_crud.generate_report(
        session, start_date=start_date, end_date=end_date
    )
    return report

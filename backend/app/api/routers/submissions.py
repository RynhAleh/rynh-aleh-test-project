from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.sessions import get_db
from app.schemas import HistoryResponse, SubmissionCreate, SubmissionResponse
from app.services.crud import create_submission, get_history

router = APIRouter(prefix="/api", tags=["submissions"])


@router.post("/submit", response_model=SubmissionResponse)
async def submit(submission: SubmissionCreate, db: AsyncSession = Depends(get_db)):
    await create_submission(
        db, submission.date, submission.first_name, submission.last_name
    )
    return {"success": True}


@router.get("/history", response_model=HistoryResponse)
async def history(
    date: date,
    first_name: str | None = None,
    last_name: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await get_history(db, date, first_name, last_name)

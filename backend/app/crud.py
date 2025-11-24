from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from .models import Submission
from datetime import date
from typing import Optional
import time
import random


def create_submission(db: Session, date: date, first_name: str, last_name: str):
    db_submission = Submission(date=date, first_name=first_name, last_name=last_name)
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_history(db: Session, filter_date: date, first_name: Optional[str] = None, last_name: Optional[str] = None):
    # Base query with filters
    query = db.query(Submission).filter(Submission.date <= filter_date)
    if first_name:
        query = query.filter(Submission.first_name == first_name)
    if last_name:
        query = query.filter(Submission.last_name == last_name)

    total = query.count()

    # Get 10 latest, sorted by date desc, then first_name, last_name
    items = query.order_by(desc(Submission.date), Submission.first_name, Submission.last_name).limit(10).all()

    # For each item, count previous same name combo with earlier date
    history_items = []
    for item in items:
        count_query = db.query(func.count()).filter(
            and_(
                Submission.first_name == item.first_name,
                Submission.last_name == item.last_name,
                Submission.date < item.date
            )
        )
        count = count_query.scalar() or 0
        history_items.append({
            "date": item.date.isoformat(),
            "first_name": item.first_name,
            "last_name": item.last_name,
            "count": count
        })

    return {"items": history_items, "total": total}

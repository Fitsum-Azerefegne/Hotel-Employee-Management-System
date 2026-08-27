from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/attendance-summary", response_model=List[schemas.DepartmentAttendanceSummary])
def attendance_summary(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    return crud.get_department_attendance_summary(db, start_date, end_date)


@router.get("/missed-shifts", response_model=List[schemas.MissedShift])
def missed_shifts(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    return crud.get_missed_shifts(db, start_date, end_date)

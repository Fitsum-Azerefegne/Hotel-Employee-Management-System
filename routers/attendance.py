from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=schemas.Attendance, status_code=201)
def record_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    if crud.get_employee(db, attendance.employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    if attendance.shift_id is not None and crud.get_shift(db, attendance.shift_id) is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return crud.create_attendance(db, attendance)


@router.get("/", response_model=List[schemas.Attendance])
def list_attendance(
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    return crud.get_attendance_records(db, employee_id, start_date, end_date)

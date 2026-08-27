from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/shifts", tags=["Shifts"])


@router.post("/", response_model=schemas.Shift, status_code=201)
def create_shift(shift: schemas.ShiftCreate, db: Session = Depends(get_db)):
    if crud.get_employee(db, shift.employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    try:
        return crud.create_shift(db, shift)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This employee already has a shift of this type on this date",
        )


@router.get("/", response_model=List[schemas.Shift])
def list_shifts(
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    return crud.get_shifts(db, employee_id, start_date, end_date)


@router.delete("/{shift_id}", status_code=204)
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_shift(db, shift_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shift not found")

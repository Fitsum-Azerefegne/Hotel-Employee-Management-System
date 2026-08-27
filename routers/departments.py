from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("/", response_model=schemas.Department, status_code=201)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)


@router.get("/", response_model=List[schemas.Department])
def list_departments(db: Session = Depends(get_db)):
    return crud.get_departments(db)

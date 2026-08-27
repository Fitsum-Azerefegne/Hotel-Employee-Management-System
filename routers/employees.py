from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/employees", tags=["Employees"])


def _validate_department_and_role(db: Session, department_id: int, role_id: int):
    if crud.get_department(db, department_id) is None:
        raise HTTPException(status_code=404, detail=f"Department {department_id} not found")
    if crud.get_role(db, role_id) is None:
        raise HTTPException(status_code=404, detail=f"Role {role_id} not found")


@router.post("/", response_model=schemas.Employee, status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    _validate_department_and_role(db, employee.department_id, employee.role_id)
    return crud.create_employee(db, employee)


@router.get("/", response_model=List[schemas.Employee])
def list_employees(
    department_id: Optional[int] = None,
    role_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_employees(db, department_id, role_id, is_active, skip, limit)


@router.get("/{employee_id}", response_model=schemas.Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.patch("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)
):
    if employee_update.department_id is not None and crud.get_department(db, employee_update.department_id) is None:
        raise HTTPException(status_code=404, detail="Department not found")
    if employee_update.role_id is not None and crud.get_role(db, employee_update.role_id) is None:
        raise HTTPException(status_code=404, detail="Role not found")
    updated = crud.update_employee(db, employee_id, employee_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")

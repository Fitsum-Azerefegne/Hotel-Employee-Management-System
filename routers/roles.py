from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=schemas.Role, status_code=201)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, role)


@router.get("/", response_model=List[schemas.Role])
def list_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db)

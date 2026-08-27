from datetime import date
from typing import List, Optional

from sqlalchemy import func, case
from sqlalchemy.orm import Session

import models
import schemas


def create_department(db: Session, department: schemas.DepartmentCreate) -> models.Department:
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def get_departments(db: Session) -> List[models.Department]:
    return db.query(models.Department).order_by(models.Department.name).all()


def get_department(db: Session, department_id: int) -> Optional[models.Department]:
    return db.query(models.Department).filter(models.Department.id == department_id).first()


def create_role(db: Session, role: schemas.RoleCreate) -> models.Role:
    db_role = models.Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session) -> List[models.Role]:
    return db.query(models.Role).order_by(models.Role.title).all()


def get_role(db: Session, role_id: int) -> Optional[models.Role]:
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employees(
    db: Session,
    department_id: Optional[int] = None,
    role_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Employee]:
    query = db.query(models.Employee)
    if department_id is not None:
        query = query.filter(models.Employee.department_id == department_id)
    if role_id is not None:
        query = query.filter(models.Employee.role_id == role_id)
    if is_active is not None:
        query = query.filter(models.Employee.is_active == is_active)
    return query.order_by(models.Employee.last_name).offset(skip).limit(limit).all()


def update_employee(
    db: Session, employee_id: int, employee_update: schemas.EmployeeUpdate
) -> Optional[models.Employee]:
    db_employee = get_employee(db, employee_id)
    if db_employee is None:
        return None
    for field, value in employee_update.model_dump(exclude_unset=True).items():
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int) -> bool:
    db_employee = get_employee(db, employee_id)
    if db_employee is None:
        return False
    db.delete(db_employee)
    db.commit()
    return True


def create_shift(db: Session, shift: schemas.ShiftCreate) -> models.Shift:
    db_shift = models.Shift(**shift.model_dump())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift


def get_shifts(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[models.Shift]:
    query = db.query(models.Shift)
    if employee_id is not None:
        query = query.filter(models.Shift.employee_id == employee_id)
    if start_date is not None:
        query = query.filter(models.Shift.shift_date >= start_date)
    if end_date is not None:
        query = query.filter(models.Shift.shift_date <= end_date)
    return query.order_by(models.Shift.shift_date).all()


def get_shift(db: Session, shift_id: int) -> Optional[models.Shift]:
    return db.query(models.Shift).filter(models.Shift.id == shift_id).first()


def delete_shift(db: Session, shift_id: int) -> bool:
    db_shift = get_shift(db, shift_id)
    if db_shift is None:
        return False
    db.delete(db_shift)
    db.commit()
    return True


def create_attendance(db: Session, attendance: schemas.AttendanceCreate) -> models.Attendance:
    db_attendance = models.Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


def get_attendance_records(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[models.Attendance]:
    query = db.query(models.Attendance)
    if employee_id is not None:
        query = query.filter(models.Attendance.employee_id == employee_id)
    if start_date is not None:
        query = query.filter(models.Attendance.attendance_date >= start_date)
    if end_date is not None:
        query = query.filter(models.Attendance.attendance_date <= end_date)
    return query.order_by(models.Attendance.attendance_date).all()


def get_department_attendance_summary(
    db: Session, start_date: date, end_date: date
) -> List[dict]:
    shifts_subq = (
        db.query(
            models.Employee.department_id.label("department_id"),
            func.count(models.Shift.id).label("total_shifts_scheduled"),
        )
        .join(models.Shift, models.Shift.employee_id == models.Employee.id)
        .filter(models.Shift.shift_date.between(start_date, end_date))
        .group_by(models.Employee.department_id)
        .subquery()
    )

    attendance_subq = (
        db.query(
            models.Employee.department_id.label("department_id"),
            func.count(models.Attendance.id).label("total_attendance_records"),
            func.sum(
                case((models.Attendance.status == models.AttendanceStatus.PRESENT, 1), else_=0)
            ).label("present_count"),
            func.sum(
                case((models.Attendance.status == models.AttendanceStatus.LATE, 1), else_=0)
            ).label("late_count"),
            func.sum(
                case((models.Attendance.status == models.AttendanceStatus.ABSENT, 1), else_=0)
            ).label("absent_count"),
        )
        .join(models.Attendance, models.Attendance.employee_id == models.Employee.id)
        .filter(models.Attendance.attendance_date.between(start_date, end_date))
        .group_by(models.Employee.department_id)
        .subquery()
    )

    rows = (
        db.query(
            models.Department.id.label("department_id"),
            models.Department.name.label("department_name"),
            func.coalesce(shifts_subq.c.total_shifts_scheduled, 0).label("total_shifts_scheduled"),
            func.coalesce(attendance_subq.c.total_attendance_records, 0).label("total_attendance_records"),
            func.coalesce(attendance_subq.c.present_count, 0).label("present_count"),
            func.coalesce(attendance_subq.c.late_count, 0).label("late_count"),
            func.coalesce(attendance_subq.c.absent_count, 0).label("absent_count"),
        )
        .outerjoin(shifts_subq, shifts_subq.c.department_id == models.Department.id)
        .outerjoin(attendance_subq, attendance_subq.c.department_id == models.Department.id)
        .order_by(models.Department.name)
        .all()
    )

    results = []
    for row in rows:
        scheduled = row.total_shifts_scheduled or 0
        present = row.present_count or 0
        late = row.late_count or 0
        rate = round(((present + late) / scheduled) * 100, 1) if scheduled else 0.0
        results.append({
            "department_id": row.department_id,
            "department_name": row.department_name,
            "total_shifts_scheduled": scheduled,
            "total_attendance_records": row.total_attendance_records or 0,
            "present_count": present,
            "late_count": late,
            "absent_count": row.absent_count or 0,
            "attendance_rate_pct": rate,
        })
    return results


def get_missed_shifts(
    db: Session, start_date: date, end_date: date
) -> List[dict]:
    rows = (
        db.query(models.Shift, models.Employee, models.Department)
        .join(models.Employee, models.Shift.employee_id == models.Employee.id)
        .join(models.Department, models.Employee.department_id == models.Department.id)
        .outerjoin(models.Attendance, models.Attendance.shift_id == models.Shift.id)
        .filter(models.Attendance.id.is_(None))
        .filter(models.Shift.shift_date.between(start_date, end_date))
        .order_by(models.Shift.shift_date)
        .all()
    )

    return [
        {
            "shift_id": shift.id,
            "employee_id": employee.id,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "department_name": department.name,
            "shift_date": shift.shift_date,
            "shift_type": shift.shift_type,
        }
        for shift, employee, department in rows
    ]

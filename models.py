from datetime import date, datetime
import enum

from sqlalchemy import (
    Column, Integer, String, Date, DateTime,
    ForeignKey, Enum, Boolean, Text, UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    LATE = "late"
    ABSENT = "absent"
    LEFT_EARLY = "left_early"
    PERMITTED = "permitted"


class ShiftType(str, enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    employees = relationship("Employee", back_populates="department")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    employees = relationship("Employee", back_populates="role")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    hire_date = Column(Date, nullable=False, default=date.today)
    is_active = Column(Boolean, nullable=False, default=True)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    department = relationship("Department", back_populates="employees")
    role = relationship("Role", back_populates="employees")
    shifts = relationship("Shift", back_populates="employee", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_date = Column(Date, nullable=False, index=True)
    shift_type = Column(Enum(ShiftType), nullable=False)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)

    employee = relationship("Employee", back_populates="shifts")
    attendance = relationship("Attendance", back_populates="shift", uselist=False)

    __table_args__ = (
        UniqueConstraint("employee_id", "shift_date", "shift_type", name="uq_employee_shift"),
    )


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=True)
    attendance_date = Column(Date, nullable=False, index=True)
    status = Column(Enum(AttendanceStatus), nullable=False)
    clock_in = Column(DateTime, nullable=True)
    clock_out = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="attendance_records")
    shift = relationship("Shift", back_populates="attendance")

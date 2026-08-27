from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict

from models import AttendanceStatus, ShiftType


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RoleBase(BaseModel):
    title: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    hire_date: date = date.today()
    is_active: bool = True
    department_id: int
    role_id: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    department_id: Optional[int] = None
    role_id: Optional[int] = None

class Employee(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    department: Department
    role: Role


class ShiftBase(BaseModel):
    employee_id: int
    shift_date: date
    shift_type: ShiftType
    start_time: str
    end_time: str

class ShiftCreate(ShiftBase):
    pass

class Shift(ShiftBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AttendanceBase(BaseModel):
    employee_id: int
    shift_id: Optional[int] = None
    attendance_date: date
    status: AttendanceStatus
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    notes: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DepartmentAttendanceSummary(BaseModel):
    department_id: int
    department_name: str
    total_shifts_scheduled: int
    total_attendance_records: int
    present_count: int
    late_count: int
    absent_count: int
    attendance_rate_pct: float


class MissedShift(BaseModel):
    shift_id: int
    employee_id: int
    employee_name: str
    department_name: str
    shift_date: date
    shift_type: ShiftType

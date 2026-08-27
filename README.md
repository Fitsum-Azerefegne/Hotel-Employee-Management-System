# Hotel Employee Management System

REST API for managing hotel employees: departments, roles, shifts, and attendance.

## Stack

- FastAPI, SQLAlchemy 2.0, SQLite, Pydantic v2, pytest

## Getting started

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the Swagger UI. Tables are created automatically on startup.

## Structure

```
main.py        app setup, mounts routers, creates tables
database.py    engine/session
models.py      ORM models
schemas.py     Pydantic request/response models
crud.py        all query logic
routers/       one file per resource
```

## API

| Resource    | Endpoints                                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------- |
| Departments | `POST /departments/`, `GET /departments/`                                                                       |
| Roles       | `POST /roles/`, `GET /roles/`                                                                                   |
| Employees   | `POST /employees/`, `GET /employees/`, `GET /employees/{id}`, `PATCH /employees/{id}`, `DELETE /employees/{id}` |
| Shifts      | `POST /shifts/`, `GET /shifts/`, `DELETE /shifts/{id}`                                                          |
| Attendance  | `POST /attendance/`, `GET /attendance/`                                                                         |
| Reports     | `GET /reports/attendance-summary`, `GET /reports/missed-shifts`                                                 |

Employee filters: `?department_id=`, `?role_id=`, `?is_active=`  
Shift/attendance filters: `?employee_id=`, `?start_date=`, `?end_date=`

Reassigning a department or role is a `PATCH /employees/{id}` with the new FK.

## Reports

Both take `?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`.

- **`/reports/attendance-summary`** — per department: shifts scheduled, attendance breakdown (present/late/absent), and attendance rate. Departments with no activity still appear with zeros.
- **`/reports/missed-shifts`** — shifts with no attendance record at all (anti-join). Catches no-call-no-shows and unlogged shifts.

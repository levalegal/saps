from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Department:
    id: Optional[int]
    name: str
    parent_id: Optional[int]
    manager_id: Optional[int]

@dataclass
class Employee:
    id: Optional[int]
    last_name: str
    first_name: str
    middle_name: Optional[str]
    department_id: Optional[int]
    position: Optional[str]
    work_phone: Optional[str]
    mobile_phone: Optional[str]
    email: Optional[str]
    birth_date: Optional[date]
    hire_date: Optional[date]
    photo: Optional[bytes]
    room: Optional[str]
    skills: Optional[str]
    manager_id: Optional[int]
    work_schedule: Optional[str]
    telegram: Optional[str]
    whatsapp: Optional[str]
    skype: Optional[str]

@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    role: str
    employee_id: Optional[int]


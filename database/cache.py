from typing import Dict, Optional, List
from database.models import Employee, Department
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = timedelta(seconds=ttl_seconds)
        self._employees_cache: Optional[List[Employee]] = None
        self._employees_timestamp: Optional[datetime] = None
        self._departments_cache: Optional[List[Department]] = None
        self._departments_timestamp: Optional[datetime] = None
        self._employee_by_id: Dict[int, Employee] = {}
        self._department_by_id: Dict[int, Department] = {}
    
    def get_employees(self) -> Optional[List[Employee]]:
        if self._is_valid(self._employees_timestamp):
            return self._employees_cache
        return None
    
    def set_employees(self, employees: List[Employee]):
        self._employees_cache = employees
        self._employees_timestamp = datetime.now()
        self._employee_by_id = {emp.id: emp for emp in employees if emp.id}
    
    def get_departments(self) -> Optional[List[Department]]:
        if self._is_valid(self._departments_timestamp):
            return self._departments_cache
        return None
    
    def set_departments(self, departments: List[Department]):
        self._departments_cache = departments
        self._departments_timestamp = datetime.now()
        self._department_by_id = {dept.id: dept for dept in departments if dept.id}
    
    def get_employee_by_id(self, emp_id: int) -> Optional[Employee]:
        return self._employee_by_id.get(emp_id)
    
    def get_department_by_id(self, dept_id: int) -> Optional[Department]:
        return self._department_by_id.get(dept_id)
    
    def invalidate_employees(self):
        self._employees_cache = None
        self._employees_timestamp = None
        self._employee_by_id = {}
    
    def invalidate_departments(self):
        self._departments_cache = None
        self._departments_timestamp = None
        self._department_by_id = {}
    
    def invalidate_all(self):
        self.invalidate_employees()
        self.invalidate_departments()
    
    def _is_valid(self, timestamp: Optional[datetime]) -> bool:
        if timestamp is None:
            return False
        return datetime.now() - timestamp < self.ttl





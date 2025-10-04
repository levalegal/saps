import json
from typing import List
from database.models import Employee, Department

class JSONExporter:
    @staticmethod
    def export_employees(employees: List[Employee], filename: str):
        data = []
        for emp in employees:
            emp_dict = {
                'id': emp.id,
                'last_name': emp.last_name,
                'first_name': emp.first_name,
                'middle_name': emp.middle_name,
                'department_id': emp.department_id,
                'position': emp.position,
                'work_phone': emp.work_phone,
                'mobile_phone': emp.mobile_phone,
                'email': emp.email,
                'birth_date': str(emp.birth_date) if emp.birth_date else None,
                'hire_date': str(emp.hire_date) if emp.hire_date else None,
                'room': emp.room,
                'skills': emp.skills,
                'manager_id': emp.manager_id,
                'work_schedule': emp.work_schedule,
                'telegram': emp.telegram,
                'whatsapp': emp.whatsapp,
                'skype': emp.skype
            }
            data.append(emp_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def import_employees(filename: str) -> List[dict]:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def export_departments(departments: List[Department], filename: str):
        data = []
        for dept in departments:
            dept_dict = {
                'id': dept.id,
                'name': dept.name,
                'parent_id': dept.parent_id,
                'manager_id': dept.manager_id
            }
            data.append(dept_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)





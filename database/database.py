import sqlite3
from typing import List, Optional, Tuple
from datetime import date
from .models import Employee, Department, User

class Database:
    def __init__(self, db_path: str = "data/employees.db"):
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
    
    def init_database(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER REFERENCES Departments(id),
                manager_id INTEGER REFERENCES Employees(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                department_id INTEGER REFERENCES Departments(id),
                position TEXT,
                work_phone TEXT,
                mobile_phone TEXT,
                email TEXT,
                birth_date DATE,
                hire_date DATE,
                photo BLOB,
                room TEXT,
                skills TEXT,
                manager_id INTEGER REFERENCES Employees(id),
                work_schedule TEXT,
                telegram TEXT,
                whatsapp TEXT,
                skype TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                employee_id INTEGER REFERENCES Employees(id)
            )
        ''')
        
        conn.commit()
        self.close()
    
    def add_employee(self, employee: Employee) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Employees (last_name, first_name, middle_name, department_id,
                                  position, work_phone, mobile_phone, email,
                                  birth_date, hire_date, photo, room, skills,
                                  manager_id, work_schedule, telegram, whatsapp, skype)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee.last_name, employee.first_name, employee.middle_name,
              employee.department_id, employee.position, employee.work_phone,
              employee.mobile_phone, employee.email, employee.birth_date,
              employee.hire_date, employee.photo, employee.room, employee.skills,
              employee.manager_id, employee.work_schedule, employee.telegram,
              employee.whatsapp, employee.skype))
        
        employee_id = cursor.lastrowid
        conn.commit()
        self.close()
        return employee_id
    
    def update_employee(self, employee: Employee):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE Employees SET last_name=?, first_name=?, middle_name=?,
                                department_id=?, position=?, work_phone=?,
                                mobile_phone=?, email=?, birth_date=?,
                                hire_date=?, photo=?, room=?, skills=?,
                                manager_id=?, work_schedule=?, telegram=?, whatsapp=?, skype=?
            WHERE id=?
        ''', (employee.last_name, employee.first_name, employee.middle_name,
              employee.department_id, employee.position, employee.work_phone,
              employee.mobile_phone, employee.email, employee.birth_date,
              employee.hire_date, employee.photo, employee.room, employee.skills,
              employee.manager_id, employee.work_schedule, employee.telegram,
              employee.whatsapp, employee.skype, employee.id))
        
        conn.commit()
        self.close()
    
    def delete_employee(self, employee_id: int):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Employees WHERE id=?', (employee_id,))
        conn.commit()
        self.close()
    
    def get_employee(self, employee_id: int) -> Optional[Employee]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Employees WHERE id=?', (employee_id,))
        row = cursor.fetchone()
        self.close()
        
        if row:
            return Employee(
                id=row['id'],
                last_name=row['last_name'],
                first_name=row['first_name'],
                middle_name=row['middle_name'],
                department_id=row['department_id'],
                position=row['position'],
                work_phone=row['work_phone'],
                mobile_phone=row['mobile_phone'],
                email=row['email'],
                birth_date=row['birth_date'],
                hire_date=row['hire_date'],
                photo=row['photo'],
                room=row['room'],
                skills=row['skills'],
                manager_id=row.get('manager_id'),
                work_schedule=row.get('work_schedule'),
                telegram=row.get('telegram'),
                whatsapp=row.get('whatsapp'),
                skype=row.get('skype')
            )
        return None
    
    def get_all_employees(self) -> List[Employee]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Employees ORDER BY last_name, first_name')
        rows = cursor.fetchall()
        self.close()
        
        employees = []
        for row in rows:
            employees.append(Employee(
                id=row['id'],
                last_name=row['last_name'],
                first_name=row['first_name'],
                middle_name=row['middle_name'],
                department_id=row['department_id'],
                position=row['position'],
                work_phone=row['work_phone'],
                mobile_phone=row['mobile_phone'],
                email=row['email'],
                birth_date=row['birth_date'],
                hire_date=row['hire_date'],
                photo=row['photo'],
                room=row['room'],
                skills=row['skills'],
                manager_id=row.get('manager_id'),
                work_schedule=row.get('work_schedule'),
                telegram=row.get('telegram'),
                whatsapp=row.get('whatsapp'),
                skype=row.get('skype')
            ))
        return employees
    
    def search_employees(self, query: str) -> List[Employee]:
        conn = self.connect()
        cursor = conn.cursor()
        
        search_pattern = f'%{query}%'
        cursor.execute('''
            SELECT * FROM Employees
            WHERE last_name LIKE ? OR first_name LIKE ? OR middle_name LIKE ?
               OR position LIKE ? OR work_phone LIKE ? OR mobile_phone LIKE ?
               OR email LIKE ?
            ORDER BY last_name, first_name
        ''', (search_pattern, search_pattern, search_pattern, search_pattern,
              search_pattern, search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        self.close()
        
        employees = []
        for row in rows:
            employees.append(Employee(
                id=row['id'],
                last_name=row['last_name'],
                first_name=row['first_name'],
                middle_name=row['middle_name'],
                department_id=row['department_id'],
                position=row['position'],
                work_phone=row['work_phone'],
                mobile_phone=row['mobile_phone'],
                email=row['email'],
                birth_date=row['birth_date'],
                hire_date=row['hire_date'],
                photo=row['photo'],
                room=row['room'],
                skills=row['skills'],
                manager_id=row.get('manager_id'),
                work_schedule=row.get('work_schedule'),
                telegram=row.get('telegram'),
                whatsapp=row.get('whatsapp'),
                skype=row.get('skype')
            ))
        return employees
    
    def filter_employees(self, department_id: Optional[int] = None,
                        position: Optional[str] = None) -> List[Employee]:
        conn = self.connect()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM Employees WHERE 1=1'
        params = []
        
        if department_id is not None:
            query += ' AND department_id=?'
            params.append(department_id)
        
        if position:
            query += ' AND position LIKE ?'
            params.append(f'%{position}%')
        
        query += ' ORDER BY last_name, first_name'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        self.close()
        
        employees = []
        for row in rows:
            employees.append(Employee(
                id=row['id'],
                last_name=row['last_name'],
                first_name=row['first_name'],
                middle_name=row['middle_name'],
                department_id=row['department_id'],
                position=row['position'],
                work_phone=row['work_phone'],
                mobile_phone=row['mobile_phone'],
                email=row['email'],
                birth_date=row['birth_date'],
                hire_date=row['hire_date'],
                photo=row['photo'],
                room=row['room'],
                skills=row['skills'],
                manager_id=row.get('manager_id'),
                work_schedule=row.get('work_schedule'),
                telegram=row.get('telegram'),
                whatsapp=row.get('whatsapp'),
                skype=row.get('skype')
            ))
        return employees
    
    def add_department(self, department: Department) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Departments (name, parent_id, manager_id)
            VALUES (?, ?, ?)
        ''', (department.name, department.parent_id, department.manager_id))
        
        department_id = cursor.lastrowid
        conn.commit()
        self.close()
        return department_id
    
    def update_department(self, department: Department):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE Departments SET name=?, parent_id=?, manager_id=?
            WHERE id=?
        ''', (department.name, department.parent_id, department.manager_id,
              department.id))
        
        conn.commit()
        self.close()
    
    def delete_department(self, department_id: int):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Departments WHERE id=?', (department_id,))
        conn.commit()
        self.close()
    
    def get_department(self, department_id: int) -> Optional[Department]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Departments WHERE id=?', (department_id,))
        row = cursor.fetchone()
        self.close()
        
        if row:
            return Department(
                id=row['id'],
                name=row['name'],
                parent_id=row['parent_id'],
                manager_id=row['manager_id']
            )
        return None
    
    def get_all_departments(self) -> List[Department]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Departments ORDER BY name')
        rows = cursor.fetchall()
        self.close()
        
        departments = []
        for row in rows:
            departments.append(Department(
                id=row['id'],
                name=row['name'],
                parent_id=row['parent_id'],
                manager_id=row['manager_id']
            ))
        return departments
    
    def add_user(self, user: User) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Users (username, password_hash, role, employee_id)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.password_hash, user.role, user.employee_id))
        
        user_id = cursor.lastrowid
        conn.commit()
        self.close()
        return user_id
    
    def get_user(self, username: str) -> Optional[User]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
        row = cursor.fetchone()
        self.close()
        
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                password_hash=row['password_hash'],
                role=row['role'],
                employee_id=row['employee_id']
            )
        return None
    
    def filter_employees_by_hire_date(self, start_date: Optional[str] = None, 
                                      end_date: Optional[str] = None) -> List[Employee]:
        conn = self.connect()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM Employees WHERE 1=1'
        params = []
        
        if start_date:
            query += ' AND hire_date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND hire_date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY hire_date DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        self.close()
        
        employees = []
        for row in rows:
            employees.append(Employee(
                id=row['id'],
                last_name=row['last_name'],
                first_name=row['first_name'],
                middle_name=row['middle_name'],
                department_id=row['department_id'],
                position=row['position'],
                work_phone=row['work_phone'],
                mobile_phone=row['mobile_phone'],
                email=row['email'],
                birth_date=row['birth_date'],
                hire_date=row['hire_date'],
                photo=row['photo'],
                room=row['room'],
                skills=row['skills'],
                manager_id=row.get('manager_id'),
                work_schedule=row.get('work_schedule'),
                telegram=row.get('telegram'),
                whatsapp=row.get('whatsapp'),
                skype=row.get('skype')
            ))
        return employees
    
    def get_employees_by_birthday_month(self, month: int) -> List[Employee]:
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM Employees
            WHERE CAST(strftime('%m', birth_date) AS INTEGER) = ?
            ORDER BY strftime('%d', birth_date)
        ''', (month,))
        
        rows = cursor.fetchall()
        self.close()
        
        employees = []
        for row in rows:
            employees.append(Employee(
                id=row['id'],
                last_name=row['last_name'],
                first_name=row['first_name'],
                middle_name=row['middle_name'],
                department_id=row['department_id'],
                position=row['position'],
                work_phone=row['work_phone'],
                mobile_phone=row['mobile_phone'],
                email=row['email'],
                birth_date=row['birth_date'],
                hire_date=row['hire_date'],
                photo=row['photo'],
                room=row['room'],
                skills=row['skills'],
                manager_id=row.get('manager_id'),
                work_schedule=row.get('work_schedule'),
                telegram=row.get('telegram'),
                whatsapp=row.get('whatsapp'),
                skype=row.get('skype')
            ))
        return employees


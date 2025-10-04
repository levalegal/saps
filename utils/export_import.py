import csv
import pandas as pd
from typing import List
from datetime import datetime
from database.models import Employee, Department
from database.database import Database
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class ExportImport:
    def __init__(self, database: Database):
        self.database = database
    
    def export_to_csv(self, filename: str, employees: List[Employee]):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'last_name', 'first_name', 'middle_name',
                         'department_id', 'position', 'work_phone', 'mobile_phone',
                         'email', 'birth_date', 'hire_date', 'room', 'skills']
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for emp in employees:
                writer.writerow({
                    'id': emp.id,
                    'last_name': emp.last_name,
                    'first_name': emp.first_name,
                    'middle_name': emp.middle_name or '',
                    'department_id': emp.department_id or '',
                    'position': emp.position or '',
                    'work_phone': emp.work_phone or '',
                    'mobile_phone': emp.mobile_phone or '',
                    'email': emp.email or '',
                    'birth_date': emp.birth_date or '',
                    'hire_date': emp.hire_date or '',
                    'room': emp.room or '',
                    'skills': emp.skills or ''
                })
    
    def import_from_csv(self, filename: str) -> int:
        count = 0
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    employee = Employee(
                        id=None,
                        last_name=row['last_name'],
                        first_name=row['first_name'],
                        middle_name=row.get('middle_name') or None,
                        department_id=int(row['department_id']) if row.get('department_id') else None,
                        position=row.get('position') or None,
                        work_phone=row.get('work_phone') or None,
                        mobile_phone=row.get('mobile_phone') or None,
                        email=row.get('email') or None,
                        birth_date=row.get('birth_date') or None,
                        hire_date=row.get('hire_date') or None,
                        photo=None,
                        room=row.get('room') or None,
                        skills=row.get('skills') or None
                    )
                    self.database.add_employee(employee)
                    count += 1
                except Exception:
                    continue
        
        return count
    
    def export_to_excel(self, filename: str, employees: List[Employee]):
        data = []
        for emp in employees:
            data.append({
                'ID': emp.id,
                'Фамилия': emp.last_name,
                'Имя': emp.first_name,
                'Отчество': emp.middle_name or '',
                'Отдел': emp.department_id or '',
                'Должность': emp.position or '',
                'Рабочий телефон': emp.work_phone or '',
                'Мобильный телефон': emp.mobile_phone or '',
                'Email': emp.email or '',
                'Дата рождения': emp.birth_date or '',
                'Дата приема': emp.hire_date or '',
                'Кабинет': emp.room or '',
                'Навыки': emp.skills or ''
            })
        
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')
    
    def import_from_excel(self, filename: str) -> int:
        df = pd.read_excel(filename, engine='openpyxl')
        count = 0
        
        column_mapping = {
            'Фамилия': 'last_name',
            'Имя': 'first_name',
            'Отчество': 'middle_name',
            'Отдел': 'department_id',
            'Должность': 'position',
            'Рабочий телефон': 'work_phone',
            'Мобильный телефон': 'mobile_phone',
            'Email': 'email',
            'Дата рождения': 'birth_date',
            'Дата приема': 'hire_date',
            'Кабинет': 'room',
            'Навыки': 'skills'
        }
        
        for _, row in df.iterrows():
            try:
                employee = Employee(
                    id=None,
                    last_name=str(row.get('Фамилия', '')),
                    first_name=str(row.get('Имя', '')),
                    middle_name=str(row.get('Отчество', '')) if pd.notna(row.get('Отчество')) else None,
                    department_id=int(row['Отдел']) if pd.notna(row.get('Отдел')) else None,
                    position=str(row.get('Должность', '')) if pd.notna(row.get('Должность')) else None,
                    work_phone=str(row.get('Рабочий телефон', '')) if pd.notna(row.get('Рабочий телефон')) else None,
                    mobile_phone=str(row.get('Мобильный телефон', '')) if pd.notna(row.get('Мобильный телефон')) else None,
                    email=str(row.get('Email', '')) if pd.notna(row.get('Email')) else None,
                    birth_date=str(row.get('Дата рождения', '')) if pd.notna(row.get('Дата рождения')) else None,
                    hire_date=str(row.get('Дата приема', '')) if pd.notna(row.get('Дата приема')) else None,
                    photo=None,
                    room=str(row.get('Кабинет', '')) if pd.notna(row.get('Кабинет')) else None,
                    skills=str(row.get('Навыки', '')) if pd.notna(row.get('Навыки')) else None
                )
                self.database.add_employee(employee)
                count += 1
            except Exception:
                continue
        
        return count
    
    def export_to_vcard(self, filename: str, employee: Employee):
        vcard = f"BEGIN:VCARD\n"
        vcard += f"VERSION:3.0\n"
        vcard += f"FN:{employee.last_name} {employee.first_name}"
        if employee.middle_name:
            vcard += f" {employee.middle_name}"
        vcard += f"\n"
        vcard += f"N:{employee.last_name};{employee.first_name}"
        if employee.middle_name:
            vcard += f";{employee.middle_name}"
        vcard += f";;\n"
        
        if employee.position:
            vcard += f"TITLE:{employee.position}\n"
        
        if employee.work_phone:
            vcard += f"TEL;TYPE=WORK:{employee.work_phone}\n"
        
        if employee.mobile_phone:
            vcard += f"TEL;TYPE=CELL:{employee.mobile_phone}\n"
        
        if employee.email:
            vcard += f"EMAIL:{employee.email}\n"
        
        if employee.birth_date:
            vcard += f"BDAY:{employee.birth_date}\n"
        
        vcard += f"END:VCARD"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(vcard)
    
    def export_to_pdf(self, filename: str, employees: List[Employee]):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=30,
        )
        
        title = Paragraph("Список сотрудников", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        data = [['ФИО', 'Должность', 'Телефон', 'Email']]
        
        for emp in employees:
            full_name = f"{emp.last_name} {emp.first_name}"
            if emp.middle_name:
                full_name += f" {emp.middle_name}"
            
            phone = emp.work_phone or emp.mobile_phone or '-'
            email = emp.email or '-'
            position = emp.position or '-'
            
            data.append([full_name, position, phone, email])
        
        table = Table(data, colWidths=[2.5*inch, 2*inch, 1.5*inch, 2*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(table)
        doc.build(elements)




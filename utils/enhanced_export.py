from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from io import BytesIO
from database.models import Employee
from typing import List
from datetime import datetime

class EnhancedExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
    def export_employees_to_pdf_with_template(self, employees: List[Employee], filename: str, 
                                               title: str = "Список сотрудников",
                                               include_photos: bool = True):
        doc = SimpleDocTemplate(filename, pagesize=A4,
                               leftMargin=15*mm, rightMargin=15*mm,
                               topMargin=15*mm, bottomMargin=15*mm)
        
        story = []
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph(title, title_style))
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=15,
            alignment=TA_CENTER
        )
        
        date_str = datetime.now().strftime('%d.%m.%Y %H:%M')
        story.append(Paragraph(f'Дата формирования: {date_str} | Всего записей: {len(employees)}', subtitle_style))
        story.append(Spacer(1, 10*mm))
        
        if include_photos:
            headers = ['Фото', '№', 'ФИО', 'Должность', 'Отдел', 'Телефон', 'Email']
            col_widths = [20*mm, 10*mm, 40*mm, 35*mm, 30*mm, 30*mm, 40*mm]
        else:
            headers = ['№', 'ФИО', 'Должность', 'Отдел', 'Телефон', 'Email']
            col_widths = [10*mm, 50*mm, 40*mm, 35*mm, 35*mm, 45*mm]
        
        data = [headers]
        
        for idx, emp in enumerate(employees, 1):
            full_name = f"{emp.last_name} {emp.first_name}"
            if emp.middle_name:
                full_name += f" {emp.middle_name}"
            
            position = emp.position or '-'
            department = '-'
            phone = emp.work_phone or emp.mobile_phone or '-'
            email = emp.email or '-'
            
            row = []
            
            if include_photos and emp.photo:
                try:
                    img = Image.open(BytesIO(emp.photo))
                    img.thumbnail((50, 50))
                    img_buffer = BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    rl_img = RLImage(img_buffer, width=15*mm, height=15*mm)
                    row.append(rl_img)
                except:
                    row.append('-')
            elif include_photos:
                row.append('-')
            
            row.extend([str(idx), full_name, position, department, phone, email])
            data.append(row)
        
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ])
        
        table.setStyle(table_style)
        story.append(table)
        
        doc.build(story)
    
    def export_employee_report(self, employee: Employee, filename: str):
        doc = SimpleDocTemplate(filename, pagesize=A4,
                               leftMargin=20*mm, rightMargin=20*mm,
                               topMargin=20*mm, bottomMargin=20*mm)
        
        story = []
        
        title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph('ЛИЧНАЯ КАРТОЧКА СОТРУДНИКА', title_style))
        
        if employee.photo:
            try:
                img = Image.open(BytesIO(employee.photo))
                img.thumbnail((150, 150))
                img_buffer = BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                rl_img = RLImage(img_buffer, width=40*mm, height=40*mm)
                story.append(rl_img)
                story.append(Spacer(1, 5*mm))
            except:
                pass
        
        full_name = f"{employee.last_name} {employee.first_name}"
        if employee.middle_name:
            full_name += f" {employee.middle_name}"
        
        name_style = ParagraphStyle(
            'Name',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3498db'),
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph(full_name, name_style))
        story.append(Spacer(1, 5*mm))
        
        info_data = [
            ['Должность:', employee.position or '-'],
            ['Рабочий телефон:', employee.work_phone or '-'],
            ['Мобильный телефон:', employee.mobile_phone or '-'],
            ['Email:', employee.email or '-'],
            ['Telegram:', employee.telegram or '-'],
            ['WhatsApp:', employee.whatsapp or '-'],
            ['Skype:', employee.skype or '-'],
            ['Кабинет:', employee.room or '-'],
            ['Рабочий график:', employee.work_schedule or '-'],
        ]
        
        if employee.birth_date:
            info_data.append(['Дата рождения:', str(employee.birth_date)])
        if employee.hire_date:
            info_data.append(['Дата приема:', str(employee.hire_date)])
        
        info_table = Table(info_data, colWidths=[50*mm, 100*mm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#34495e')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ]))
        
        story.append(info_table)
        
        if employee.skills:
            story.append(Spacer(1, 10*mm))
            
            skills_title = ParagraphStyle(
                'SkillsTitle',
                parent=self.styles['Heading3'],
                fontSize=14,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            
            story.append(Paragraph('Навыки и компетенции:', skills_title))
            
            skills_style = ParagraphStyle(
                'Skills',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=10
            )
            
            story.append(Paragraph(employee.skills, skills_style))
        
        story.append(Spacer(1, 15*mm))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#95a5a6'),
            alignment=TA_CENTER
        )
        
        date_str = datetime.now().strftime('%d.%m.%Y %H:%M')
        story.append(Paragraph(f'Документ сформирован: {date_str}', footer_style))
        
        doc.build(story)




from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGroupBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database.database import Database

class StatisticsWidget(QWidget):
    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        title_label = QLabel('Статистика')
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        self.total_employees_label = QLabel('Всего сотрудников: 0')
        layout.addWidget(self.total_employees_label)
        
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator1)
        
        departments_group = QGroupBox('По отделам')
        self.departments_layout = QVBoxLayout()
        departments_group.setLayout(self.departments_layout)
        layout.addWidget(departments_group)
        
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator2)
        
        self.avg_age_label = QLabel('Средний возраст: -')
        layout.addWidget(self.avg_age_label)
        
        self.with_photo_label = QLabel('С фото: 0 (0%)')
        layout.addWidget(self.with_photo_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.update_statistics()
    
    def update_statistics(self):
        employees = self.database.get_all_employees()
        departments = self.database.get_all_departments()
        
        self.total_employees_label.setText(f'Всего сотрудников: {len(employees)}')
        
        while self.departments_layout.count():
            item = self.departments_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        dept_counts = {}
        for emp in employees:
            if emp.department_id:
                dept_counts[emp.department_id] = dept_counts.get(emp.department_id, 0) + 1
        
        for dept in departments:
            count = dept_counts.get(dept.id, 0)
            dept_label = QLabel(f'{dept.name}: {count}')
            self.departments_layout.addWidget(dept_label)
        
        if not departments:
            no_dept_label = QLabel('Нет отделов')
            no_dept_label.setStyleSheet('color: gray; font-style: italic;')
            self.departments_layout.addWidget(no_dept_label)
        
        from datetime import datetime
        ages = []
        for emp in employees:
            if emp.birth_date:
                try:
                    birth_year = int(str(emp.birth_date).split('-')[0])
                    age = datetime.now().year - birth_year
                    if 18 <= age <= 100:
                        ages.append(age)
                except:
                    pass
        
        if ages:
            avg_age = sum(ages) / len(ages)
            self.avg_age_label.setText(f'Средний возраст: {avg_age:.1f} лет')
        else:
            self.avg_age_label.setText('Средний возраст: -')
        
        with_photo = sum(1 for emp in employees if emp.photo)
        if employees:
            percent = (with_photo / len(employees)) * 100
            self.with_photo_label.setText(f'С фото: {with_photo} ({percent:.1f}%)')
        else:
            self.with_photo_label.setText('С фото: 0 (0%)')





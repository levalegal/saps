from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QDateEdit,
                             QFormLayout, QCheckBox)
from PyQt6.QtCore import QDate
from database.database import Database

class AdvancedSearchDialog(QDialog):
    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        self.search_criteria = {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Расширенный поиск')
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.fio_input = QLineEdit()
        self.fio_input.setPlaceholderText('Введите ФИО...')
        form_layout.addRow('ФИО:', self.fio_input)
        
        self.department_combo = QComboBox()
        self.department_combo.addItem('Любой', None)
        departments = self.database.get_all_departments()
        for dept in departments:
            self.department_combo.addItem(dept.name, dept.id)
        form_layout.addRow('Отдел:', self.department_combo)
        
        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText('Введите должность...')
        form_layout.addRow('Должность:', self.position_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Введите email...')
        form_layout.addRow('Email:', self.email_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Введите телефон...')
        form_layout.addRow('Телефон:', self.phone_input)
        
        self.skills_input = QLineEdit()
        self.skills_input.setPlaceholderText('Введите навыки...')
        form_layout.addRow('Навыки:', self.skills_input)
        
        date_layout = QHBoxLayout()
        self.use_hire_date = QCheckBox()
        date_layout.addWidget(self.use_hire_date)
        
        self.hire_date_from = QDateEdit()
        self.hire_date_from.setCalendarPopup(True)
        self.hire_date_from.setDate(QDate.currentDate().addYears(-5))
        date_layout.addWidget(QLabel('С:'))
        date_layout.addWidget(self.hire_date_from)
        
        self.hire_date_to = QDateEdit()
        self.hire_date_to.setCalendarPopup(True)
        self.hire_date_to.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel('По:'))
        date_layout.addWidget(self.hire_date_to)
        
        form_layout.addRow('Дата приема:', date_layout)
        
        self.has_photo = QCheckBox('Только с фото')
        form_layout.addRow('', self.has_photo)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        
        search_button = QPushButton('Найти')
        search_button.clicked.connect(self.accept)
        button_layout.addWidget(search_button)
        
        clear_button = QPushButton('Очистить')
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_button)
        
        cancel_button = QPushButton('Отмена')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def clear_fields(self):
        self.fio_input.clear()
        self.department_combo.setCurrentIndex(0)
        self.position_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.skills_input.clear()
        self.use_hire_date.setChecked(False)
        self.has_photo.setChecked(False)
    
    def get_search_criteria(self):
        criteria = {}
        
        if self.fio_input.text().strip():
            criteria['fio'] = self.fio_input.text().strip()
        
        if self.department_combo.currentData():
            criteria['department_id'] = self.department_combo.currentData()
        
        if self.position_input.text().strip():
            criteria['position'] = self.position_input.text().strip()
        
        if self.email_input.text().strip():
            criteria['email'] = self.email_input.text().strip()
        
        if self.phone_input.text().strip():
            criteria['phone'] = self.phone_input.text().strip()
        
        if self.skills_input.text().strip():
            criteria['skills'] = self.skills_input.text().strip()
        
        if self.use_hire_date.isChecked():
            criteria['hire_date_from'] = self.hire_date_from.date().toString('yyyy-MM-dd')
            criteria['hire_date_to'] = self.hire_date_to.date().toString('yyyy-MM-dd')
        
        if self.has_photo.isChecked():
            criteria['has_photo'] = True
        
        return criteria





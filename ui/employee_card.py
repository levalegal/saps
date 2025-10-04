from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QScrollArea, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from database.models import Employee
from database.database import Database

class EmployeeCard(QWidget):
    call_requested = pyqtSignal(str)
    email_requested = pyqtSignal(str)
    qr_requested = pyqtSignal(Employee)
    
    def __init__(self, employee: Employee, database: Database):
        super().__init__()
        self.employee = employee
        self.database = database
        self.init_ui()
    
    def init_ui(self):
        self.setMinimumWidth(400)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        photo_label = QLabel()
        photo_label.setFixedSize(150, 150)
        photo_label.setStyleSheet('border: 2px solid #ccc; border-radius: 5px;')
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if self.employee.photo:
            pixmap = QPixmap()
            pixmap.loadFromData(self.employee.photo)
            scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, 
                                         Qt.TransformationMode.SmoothTransformation)
            photo_label.setPixmap(scaled_pixmap)
        else:
            photo_label.setText('Нет фото')
        
        layout.addWidget(photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        full_name = f"{self.employee.last_name} {self.employee.first_name}"
        if self.employee.middle_name:
            full_name += f" {self.employee.middle_name}"
        
        name_label = QLabel(full_name)
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        
        if self.employee.position:
            position_label = QLabel(self.employee.position)
            position_font = QFont()
            position_font.setPointSize(11)
            position_label.setFont(position_font)
            position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            position_label.setStyleSheet('color: #666;')
            layout.addWidget(position_label)
        
        if self.employee.department_id:
            department = self.database.get_department(self.employee.department_id)
            if department:
                dept_label = QLabel(f"Отдел: {department.name}")
                dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                dept_label.setStyleSheet('color: #666;')
                layout.addWidget(dept_label)
        
        contact_group = QGroupBox("Контактная информация")
        contact_layout = QVBoxLayout()
        
        if self.employee.work_phone:
            work_phone_layout = QHBoxLayout()
            work_phone_label = QLabel(f"Рабочий телефон: {self.employee.work_phone}")
            work_phone_layout.addWidget(work_phone_label)
            
            call_button = QPushButton("Позвонить")
            call_button.clicked.connect(lambda: self.call_requested.emit(self.employee.work_phone))
            call_button.setMaximumWidth(100)
            work_phone_layout.addWidget(call_button)
            
            contact_layout.addLayout(work_phone_layout)
        
        if self.employee.mobile_phone:
            mobile_phone_label = QLabel(f"Мобильный телефон: {self.employee.mobile_phone}")
            contact_layout.addWidget(mobile_phone_label)
        
        if self.employee.email:
            email_layout = QHBoxLayout()
            email_label = QLabel(f"Email: {self.employee.email}")
            email_layout.addWidget(email_label)
            
            email_button = QPushButton("Написать")
            email_button.clicked.connect(lambda: self.email_requested.emit(self.employee.email))
            email_button.setMaximumWidth(100)
            email_layout.addWidget(email_button)
            
            contact_layout.addLayout(email_layout)
        
        if self.employee.room:
            room_label = QLabel(f"Кабинет: {self.employee.room}")
            contact_layout.addWidget(room_label)
        
        if self.employee.telegram:
            telegram_label = QLabel(f"Telegram: {self.employee.telegram}")
            contact_layout.addWidget(telegram_label)
        
        if self.employee.whatsapp:
            whatsapp_label = QLabel(f"WhatsApp: {self.employee.whatsapp}")
            contact_layout.addWidget(whatsapp_label)
        
        if self.employee.skype:
            skype_label = QLabel(f"Skype: {self.employee.skype}")
            contact_layout.addWidget(skype_label)
        
        contact_group.setLayout(contact_layout)
        layout.addWidget(contact_group)
        
        additional_group = QGroupBox("Дополнительная информация")
        additional_layout = QVBoxLayout()
        
        if self.employee.birth_date:
            birth_date_label = QLabel(f"Дата рождения: {self.employee.birth_date}")
            additional_layout.addWidget(birth_date_label)
        
        if self.employee.hire_date:
            hire_date_label = QLabel(f"Дата приема на работу: {self.employee.hire_date}")
            additional_layout.addWidget(hire_date_label)
        
        if self.employee.manager_id:
            manager = self.database.get_employee(self.employee.manager_id)
            if manager:
                manager_name = f"{manager.last_name} {manager.first_name}"
                if manager.middle_name:
                    manager_name += f" {manager.middle_name}"
                manager_label = QLabel(f"Руководитель: {manager_name}")
                additional_layout.addWidget(manager_label)
        
        if self.employee.work_schedule:
            schedule_label = QLabel(f"Рабочий график: {self.employee.work_schedule}")
            additional_layout.addWidget(schedule_label)
        
        if self.employee.skills:
            skills_label = QLabel("Навыки:")
            additional_layout.addWidget(skills_label)
            
            skills_text = QTextEdit()
            skills_text.setPlainText(self.employee.skills)
            skills_text.setReadOnly(True)
            skills_text.setMaximumHeight(100)
            additional_layout.addWidget(skills_text)
        
        additional_group.setLayout(additional_layout)
        layout.addWidget(additional_group)
        
        button_layout = QHBoxLayout()
        
        qr_button = QPushButton("Сгенерировать QR-визитку")
        qr_button.clicked.connect(lambda: self.qr_requested.emit(self.employee))
        button_layout.addWidget(qr_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)


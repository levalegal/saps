from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QGroupBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QPixmap, QFont, QPainter, QPainterPath, QDesktopServices
from database.models import Employee
from database.database import Database
import webbrowser

class RoundedPhotoLabel(QLabel):
    def __init__(self, size=200, parent=None):
        super().__init__(parent)
        self.photo_size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                border: 4px solid #3498db;
                border-radius: {size//2}px;
                background-color: #ecf0f1;
            }}
        """)
    
    def set_photo(self, photo_data: bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(photo_data)
        
        scaled = pixmap.scaled(
            self.photo_size, 
            self.photo_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        
        rounded = QPixmap(self.photo_size, self.photo_size)
        rounded.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addEllipse(0, 0, self.photo_size, self.photo_size)
        painter.setClipPath(path)
        
        x = (scaled.width() - self.photo_size) // 2
        y = (scaled.height() - self.photo_size) // 2
        painter.drawPixmap(-x, -y, scaled)
        painter.end()
        
        self.setPixmap(rounded)

class ClickableContactLabel(QLabel):
    def __init__(self, text, action_type, value, parent=None):
        super().__init__(text, parent)
        self.action_type = action_type
        self.value = value
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_style(False)
        
    def update_style(self, hovered):
        if hovered:
            self.setStyleSheet("""
                QLabel {
                    color: #2980b9;
                    font-size: 11pt;
                    text-decoration: underline;
                    background-color: #e3f2fd;
                    padding: 8px;
                    border-radius: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    color: #3498db;
                    font-size: 11pt;
                    padding: 8px;
                    border-radius: 5px;
                }
            """)
    
    def enterEvent(self, event):
        self.update_style(True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.update_style(False)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.action_type == 'email':
                QDesktopServices.openUrl(QUrl(f"mailto:{self.value}"))
            elif self.action_type == 'phone':
                webbrowser.open(f"tel:{self.value}")
            elif self.action_type == 'telegram':
                webbrowser.open(f"https://t.me/{self.value.lstrip('@')}")
            elif self.action_type == 'whatsapp':
                clean_phone = ''.join(filter(str.isdigit, self.value))
                webbrowser.open(f"https://wa.me/{clean_phone}")
            elif self.action_type == 'skype':
                webbrowser.open(f"skype:{self.value}?chat")

class ModernEmployeeCard(QWidget):
    qr_requested = pyqtSignal(Employee)
    
    def __init__(self, employee: Employee, database: Database):
        super().__init__()
        self.employee = employee
        self.database = database
        self.init_ui()
    
    def init_ui(self):
        self.setMinimumWidth(450)
        
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #e1e8ed;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: bold;
                font-size: 11pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                margin-left: 10px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 10pt;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
            }
        """)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        photo_label = RoundedPhotoLabel(180)
        if self.employee.photo:
            photo_label.set_photo(self.employee.photo)
        else:
            photo_label.setText("📷\nНет фото")
            photo_label.setStyleSheet("""
                QLabel {
                    border: 4px dashed #bdc3c7;
                    border-radius: 90px;
                    background-color: #ecf0f1;
                    color: #7f8c8d;
                    font-size: 12pt;
                }
            """)
        
        layout.addWidget(photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        full_name = f"{self.employee.last_name} {self.employee.first_name}"
        if self.employee.middle_name:
            full_name += f" {self.employee.middle_name}"
        
        name_label = QLabel(full_name)
        name_font = QFont()
        name_font.setPointSize(16)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(name_label)
        
        if self.employee.position:
            position_label = QLabel(self.employee.position)
            position_font = QFont()
            position_font.setPointSize(12)
            position_label.setFont(position_font)
            position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            position_label.setStyleSheet("color: #7f8c8d; padding: 5px;")
            layout.addWidget(position_label)
        
        if self.employee.department_id:
            dept = self.database.get_department(self.employee.department_id)
            if dept:
                dept_label = QLabel(f"🏢 {dept.name}")
                dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                dept_label.setStyleSheet("""
                    color: #3498db; 
                    font-size: 11pt; 
                    padding: 8px;
                    background-color: #e3f2fd;
                    border-radius: 6px;
                """)
                layout.addWidget(dept_label)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #bdc3c7;")
        layout.addWidget(separator)
        
        contact_group = QGroupBox('📞 Контакты')
        contact_layout = QVBoxLayout()
        contact_layout.setSpacing(8)
        
        if self.employee.work_phone:
            phone_label = ClickableContactLabel(
                f"📞 Рабочий: {self.employee.work_phone}",
                'phone',
                self.employee.work_phone
            )
            contact_layout.addWidget(phone_label)
        
        if self.employee.mobile_phone:
            mobile_label = ClickableContactLabel(
                f"📱 Мобильный: {self.employee.mobile_phone}",
                'phone',
                self.employee.mobile_phone
            )
            contact_layout.addWidget(mobile_label)
        
        if self.employee.email:
            email_label = ClickableContactLabel(
                f"📧 Email: {self.employee.email}",
                'email',
                self.employee.email
            )
            contact_layout.addWidget(email_label)
        
        if self.employee.telegram:
            telegram_label = ClickableContactLabel(
                f"✈️ Telegram: {self.employee.telegram}",
                'telegram',
                self.employee.telegram
            )
            contact_layout.addWidget(telegram_label)
        
        if self.employee.whatsapp:
            whatsapp_label = ClickableContactLabel(
                f"💬 WhatsApp: {self.employee.whatsapp}",
                'whatsapp',
                self.employee.whatsapp
            )
            contact_layout.addWidget(whatsapp_label)
        
        if self.employee.skype:
            skype_label = ClickableContactLabel(
                f"📹 Skype: {self.employee.skype}",
                'skype',
                self.employee.skype
            )
            contact_layout.addWidget(skype_label)
        
        if contact_layout.count() == 0:
            no_contact_label = QLabel("Контактная информация не указана")
            no_contact_label.setStyleSheet("color: #95a5a6; font-style: italic;")
            contact_layout.addWidget(no_contact_label)
        
        contact_group.setLayout(contact_layout)
        layout.addWidget(contact_group)
        
        additional_group = QGroupBox('ℹ️ Дополнительная информация')
        additional_layout = QVBoxLayout()
        additional_layout.setSpacing(8)
        
        if self.employee.birth_date:
            from datetime import datetime
            birth_date = datetime.strptime(str(self.employee.birth_date), '%Y-%m-%d')
            age = (datetime.now() - birth_date).days // 365
            birth_label = QLabel(f"🎂 Дата рождения: {birth_date.strftime('%d.%m.%Y')} ({age} лет)")
            additional_layout.addWidget(birth_label)
        
        if self.employee.hire_date:
            hire_date = datetime.strptime(str(self.employee.hire_date), '%Y-%m-%d')
            years = (datetime.now() - hire_date).days // 365
            hire_label = QLabel(f"📅 Дата приема: {hire_date.strftime('%d.%m.%Y')} ({years} лет в компании)")
            additional_layout.addWidget(hire_label)
        
        if self.employee.manager_id:
            manager = self.database.get_employee(self.employee.manager_id)
            if manager:
                manager_name = f"{manager.last_name} {manager.first_name}"
                if manager.middle_name:
                    manager_name += f" {manager.middle_name}"
                manager_label = QLabel(f"👔 Руководитель: {manager_name}")
                additional_layout.addWidget(manager_label)
        
        if self.employee.work_schedule:
            schedule_label = QLabel(f"🕐 График: {self.employee.work_schedule}")
            additional_layout.addWidget(schedule_label)
        
        if self.employee.room:
            room_label = QLabel(f"🚪 Кабинет: {self.employee.room}")
            additional_layout.addWidget(room_label)
        
        if self.employee.skills:
            skills_label = QLabel(f"💼 Навыки:\n{self.employee.skills}")
            skills_label.setWordWrap(True)
            skills_label.setStyleSheet("""
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 6px;
                border-left: 4px solid #3498db;
            """)
            additional_layout.addWidget(skills_label)
        
        if additional_layout.count() == 0:
            no_info_label = QLabel("Дополнительная информация не указана")
            no_info_label.setStyleSheet("color: #95a5a6; font-style: italic;")
            additional_layout.addWidget(no_info_label)
        
        additional_group.setLayout(additional_layout)
        layout.addWidget(additional_group)
        
        qr_button = QPushButton('📱 Показать QR-код')
        qr_button.clicked.connect(lambda: self.qr_requested.emit(self.employee))
        layout.addWidget(qr_button)
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)




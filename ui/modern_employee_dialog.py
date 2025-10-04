from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QComboBox,
                             QDateEdit, QFileDialog, QFormLayout, QTabWidget,
                             QWidget, QScrollArea, QFrame)
from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QPainter, QPen, QColor
from database.models import Employee, Department
from database.database import Database
from utils.validators import Validators
from typing import Optional

class DragDropPhotoLabel(QLabel):
    photo_dropped = pyqtSignal(bytes)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFixedSize(180, 180)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_data = None
        self.apply_style()
        
    def apply_style(self):
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #3498db;
                border-radius: 90px;
                background-color: #ecf0f1;
                color: #7f8c8d;
                font-size: 10pt;
            }
        """)
        self.setText("📷\nПеретащите фото\nили\nнажмите для выбора")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            filename, _ = QFileDialog.getOpenFileName(
                self, 
                'Выберите фото', 
                '', 
                'Изображения (*.png *.jpg *.jpeg *.bmp)'
            )
            
            if filename:
                with open(filename, 'rb') as f:
                    self.photo_data = f.read()
                self.load_photo(self.photo_data)
                self.photo_dropped.emit(self.photo_data)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 3px dashed #27ae60;
                    border-radius: 90px;
                    background-color: #d5f4e6;
                    color: #27ae60;
                    font-size: 10pt;
                }
            """)
    
    def dragLeaveEvent(self, event):
        self.apply_style()
    
    def dropEvent(self, event: QDropEvent):
        files = event.mimeData().urls()
        if files:
            file_path = files[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                with open(file_path, 'rb') as f:
                    self.photo_data = f.read()
                self.load_photo(self.photo_data)
                self.photo_dropped.emit(self.photo_data)
        self.apply_style()
    
    def load_photo(self, photo_data: bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(photo_data)
        
        scaled_pixmap = pixmap.scaled(
            self.width() - 10, 
            self.height() - 10, 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        
        rounded_pixmap = QPixmap(scaled_pixmap.size())
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QPixmap(scaled_pixmap))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(rounded_pixmap.rect())
        painter.end()
        
        self.setPixmap(rounded_pixmap)
        self.setStyleSheet("""
            QLabel {
                border: 3px solid #3498db;
                border-radius: 90px;
                background-color: white;
            }
        """)

class ValidatedLineEdit(QLineEdit):
    def __init__(self, validator_func=None, parent=None):
        super().__init__(parent)
        self.validator_func = validator_func
        self.textChanged.connect(self.validate_input)
        self.default_style = """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """
        self.setStyleSheet(self.default_style)
    
    def validate_input(self):
        if not self.validator_func or not self.text().strip():
            self.setStyleSheet(self.default_style)
            return
        
        valid, msg = self.validator_func(self.text().strip())
        if valid:
            self.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #27ae60;
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 10pt;
                    background-color: #eafaf1;
                }
            """)
            self.setToolTip("✅ Корректно")
        else:
            self.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #e74c3c;
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 10pt;
                    background-color: #fadbd8;
                }
            """)
            self.setToolTip(f"❌ {msg}")

class ModernEmployeeDialog(QDialog):
    def __init__(self, database: Database, employee: Optional[Employee] = None, parent=None):
        super().__init__(parent)
        self.database = database
        self.employee = employee
        self.photo_data = None
        self.init_ui()
        
        if employee:
            self.load_employee_data()
    
    def init_ui(self):
        title = '✏️ Редактировать сотрудника' if self.employee else '➕ Добавить сотрудника'
        self.setWindowTitle(title)
        self.setMinimumSize(700, 600)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QTabWidget::pane {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: white;
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 12px 25px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 11pt;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #3498db;
                border: 2px solid #e1e8ed;
                border-bottom: 2px solid white;
            }
            QTabBar::tab:hover {
                background-color: #d5dbdb;
            }
            QLabel {
                font-size: 10pt;
                color: #2c3e50;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 11pt;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
            }
            QPushButton#cancelButton {
                background-color: #95a5a6;
            }
            QPushButton#cancelButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        tabs = QTabWidget()
        
        basic_tab = self.create_basic_tab()
        tabs.addTab(basic_tab, "📋 Основное")
        
        contact_tab = self.create_contact_tab()
        tabs.addTab(contact_tab, "📞 Контакты")
        
        additional_tab = self.create_additional_tab()
        tabs.addTab(additional_tab, "ℹ️ Дополнительно")
        
        main_layout.addWidget(tabs)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton('💾 Сохранить')
        save_button.clicked.connect(self.save)
        save_button.setMinimumWidth(150)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton('❌ Отмена')
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumWidth(150)
        button_layout.addWidget(cancel_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def create_basic_tab(self):
        tab = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        left_layout = QVBoxLayout()
        
        self.photo_label = DragDropPhotoLabel()
        self.photo_label.photo_dropped.connect(self.on_photo_dropped)
        left_layout.addWidget(self.photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addStretch()
        
        layout.addLayout(left_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.last_name_input = ValidatedLineEdit(lambda x: Validators.validate_required(x, 'Фамилия'))
        form_layout.addRow('Фамилия*:', self.last_name_input)
        
        self.first_name_input = ValidatedLineEdit(lambda x: Validators.validate_required(x, 'Имя'))
        form_layout.addRow('Имя*:', self.first_name_input)
        
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('Отчество:', self.middle_name_input)
        
        self.department_combo = QComboBox()
        self.department_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        self.department_combo.addItem('🏢 Не выбрано', None)
        departments = self.database.get_all_departments()
        for dept in departments:
            self.department_combo.addItem(f"🏢 {dept.name}", dept.id)
        form_layout.addRow('Отдел:', self.department_combo)
        
        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText('Например: Ведущий разработчик')
        self.position_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('Должность:', self.position_input)
        
        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate.currentDate())
        self.birth_date_input.setSpecialValueText('Не указано')
        self.birth_date_input.setStyleSheet("""
            QDateEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('🎂 Дата рождения:', self.birth_date_input)
        
        self.hire_date_input = QDateEdit()
        self.hire_date_input.setCalendarPopup(True)
        self.hire_date_input.setDate(QDate.currentDate())
        self.hire_date_input.setSpecialValueText('Не указано')
        self.hire_date_input.setStyleSheet("""
            QDateEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('📅 Дата приема:', self.hire_date_input)
        
        layout.addLayout(form_layout, 2)
        
        tab.setLayout(layout)
        return tab
    
    def create_contact_tab(self):
        tab = QWidget()
        form_layout = QFormLayout()
        form_layout.setContentsMargins(40, 30, 40, 30)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.work_phone_input = ValidatedLineEdit(Validators.validate_phone)
        self.work_phone_input.setPlaceholderText('+7(XXX)XXX-XX-XX')
        form_layout.addRow('📞 Рабочий телефон:', self.work_phone_input)
        
        self.mobile_phone_input = ValidatedLineEdit(Validators.validate_phone)
        self.mobile_phone_input.setPlaceholderText('+7(XXX)XXX-XX-XX')
        form_layout.addRow('📱 Мобильный телефон:', self.mobile_phone_input)
        
        self.email_input = ValidatedLineEdit(Validators.validate_email)
        self.email_input.setPlaceholderText('example@company.ru')
        form_layout.addRow('📧 Email:', self.email_input)
        
        self.telegram_input = ValidatedLineEdit(Validators.validate_telegram)
        self.telegram_input.setPlaceholderText('@username')
        form_layout.addRow('✈️ Telegram:', self.telegram_input)
        
        self.whatsapp_input = ValidatedLineEdit(Validators.validate_phone)
        self.whatsapp_input.setPlaceholderText('+7XXXXXXXXXX')
        form_layout.addRow('💬 WhatsApp:', self.whatsapp_input)
        
        self.skype_input = QLineEdit()
        self.skype_input.setPlaceholderText('skype_username')
        self.skype_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('📹 Skype:', self.skype_input)
        
        form_layout.addRow(QLabel(""))
        
        tab.setLayout(form_layout)
        return tab
    
    def create_additional_tab(self):
        tab = QWidget()
        form_layout = QFormLayout()
        form_layout.setContentsMargins(40, 30, 40, 30)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.manager_combo = QComboBox()
        self.manager_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        self.manager_combo.addItem('👤 Нет руководителя', None)
        all_employees = self.database.get_all_employees()
        for emp in all_employees:
            full_name = f"{emp.last_name} {emp.first_name}"
            if emp.middle_name:
                full_name += f" {emp.middle_name}"
            self.manager_combo.addItem(f"👤 {full_name}", emp.id)
        form_layout.addRow('👔 Руководитель:', self.manager_combo)
        
        self.work_schedule_input = QLineEdit()
        self.work_schedule_input.setPlaceholderText('Например: Пн-Пт 9:00-18:00')
        self.work_schedule_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('🕐 Рабочий график:', self.work_schedule_input)
        
        self.room_input = QLineEdit()
        self.room_input.setPlaceholderText('Например: 401')
        self.room_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('🚪 Кабинет:', self.room_input)
        
        self.skills_input = QTextEdit()
        self.skills_input.setMaximumHeight(120)
        self.skills_input.setPlaceholderText('Например: Python, JavaScript, SQL...')
        self.skills_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        form_layout.addRow('💼 Навыки:', self.skills_input)
        
        tab.setLayout(form_layout)
        return tab
    
    def on_photo_dropped(self, photo_data: bytes):
        self.photo_data = photo_data
    
    def load_employee_data(self):
        if not self.employee:
            return
        
        self.last_name_input.setText(self.employee.last_name)
        self.first_name_input.setText(self.employee.first_name)
        self.middle_name_input.setText(self.employee.middle_name or '')
        
        if self.employee.department_id:
            for i in range(self.department_combo.count()):
                if self.department_combo.itemData(i) == self.employee.department_id:
                    self.department_combo.setCurrentIndex(i)
                    break
        
        self.position_input.setText(self.employee.position or '')
        self.work_phone_input.setText(self.employee.work_phone or '')
        self.mobile_phone_input.setText(self.employee.mobile_phone or '')
        self.email_input.setText(self.employee.email or '')
        
        if self.employee.birth_date:
            date_parts = str(self.employee.birth_date).split('-')
            if len(date_parts) == 3:
                self.birth_date_input.setDate(
                    QDate(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
                )
        
        if self.employee.hire_date:
            date_parts = str(self.employee.hire_date).split('-')
            if len(date_parts) == 3:
                self.hire_date_input.setDate(
                    QDate(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
                )
        
        self.room_input.setText(self.employee.room or '')
        self.skills_input.setPlainText(self.employee.skills or '')
        
        if self.employee.manager_id:
            for i in range(self.manager_combo.count()):
                if self.manager_combo.itemData(i) == self.employee.manager_id:
                    self.manager_combo.setCurrentIndex(i)
                    break
        
        self.work_schedule_input.setText(self.employee.work_schedule or '')
        self.telegram_input.setText(self.employee.telegram or '')
        self.whatsapp_input.setText(self.employee.whatsapp or '')
        self.skype_input.setText(self.employee.skype or '')
        
        if self.employee.photo:
            self.photo_data = self.employee.photo
            self.photo_label.load_photo(self.employee.photo)
    
    def save(self):
        from ui.toast_notification import show_toast
        
        last_name = self.last_name_input.text().strip()
        first_name = self.first_name_input.text().strip()
        
        valid, msg = Validators.validate_required(last_name, 'Фамилия')
        if not valid:
            show_toast(self, msg, "error")
            return
        
        valid, msg = Validators.validate_required(first_name, 'Имя')
        if not valid:
            show_toast(self, msg, "error")
            return
        
        email = self.email_input.text().strip()
        if email:
            valid, msg = Validators.validate_email(email)
            if not valid:
                show_toast(self, msg, "error")
                return
        
        work_phone = self.work_phone_input.text().strip()
        if work_phone:
            valid, msg = Validators.validate_phone(work_phone)
            if not valid:
                show_toast(self, msg, "error")
                return
        
        mobile_phone = self.mobile_phone_input.text().strip()
        if mobile_phone:
            valid, msg = Validators.validate_phone(mobile_phone)
            if not valid:
                show_toast(self, msg, "error")
                return
        
        telegram = self.telegram_input.text().strip()
        if telegram:
            valid, msg = Validators.validate_telegram(telegram)
            if not valid:
                show_toast(self, msg, "error")
                return
        
        department_id = self.department_combo.currentData()
        
        birth_date = None
        if self.birth_date_input.date() != QDate.currentDate():
            birth_date = self.birth_date_input.date().toString('yyyy-MM-dd')
        
        hire_date = None
        if self.hire_date_input.date() != QDate.currentDate():
            hire_date = self.hire_date_input.date().toString('yyyy-MM-dd')
        
        manager_id = self.manager_combo.currentData()
        
        employee = Employee(
            id=self.employee.id if self.employee else None,
            last_name=last_name,
            first_name=first_name,
            middle_name=self.middle_name_input.text().strip() or None,
            department_id=department_id,
            position=self.position_input.text().strip() or None,
            work_phone=self.work_phone_input.text().strip() or None,
            mobile_phone=self.mobile_phone_input.text().strip() or None,
            email=self.email_input.text().strip() or None,
            birth_date=birth_date,
            hire_date=hire_date,
            photo=self.photo_data,
            room=self.room_input.text().strip() or None,
            skills=self.skills_input.toPlainText().strip() or None,
            manager_id=manager_id,
            work_schedule=self.work_schedule_input.text().strip() or None,
            telegram=self.telegram_input.text().strip() or None,
            whatsapp=self.whatsapp_input.text().strip() or None,
            skype=self.skype_input.text().strip() or None
        )
        
        try:
            if self.employee:
                self.database.update_employee(employee)
            else:
                self.database.add_employee(employee)
            
            self.accept()
        except Exception as e:
            show_toast(self, f'Не удалось сохранить: {str(e)}', "error")




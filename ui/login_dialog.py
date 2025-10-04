from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette
from auth.auth import AuthManager

class LoginDialog(QDialog):
    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        self.setWindowTitle('Вход в систему - Каталог контактов')
        self.setFixedSize(500, 450)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Контейнер с закругленными углами
        container = QFrame()
        container.setObjectName("container")
        
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(40, 35, 40, 35)
        
        # Кнопка закрытия
        close_btn = QPushButton('✕')
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(35, 35)
        close_btn.clicked.connect(self.reject)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(close_btn)
        close_layout.setContentsMargins(0, 0, 0, 10)
        main_layout.addLayout(close_layout)
        
        # Заголовок с иконкой
        title_label = QLabel('👥 Каталог контактов\nсотрудников')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont('Segoe UI', 22, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet('color: #1a1a2e; margin-bottom: 5px; line-height: 1.3;')
        main_layout.addWidget(title_label)
        
        # Версия
        version_label = QLabel('Улучшенный интерфейс с анимациями')
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet('''
            color: #6c757d; 
            font-size: 10pt;
            padding: 8px 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e3f2fd, stop:1 #f3e5f5);
            border-radius: 15px;
            font-weight: 500;
        ''')
        main_layout.addWidget(version_label)
        
        # Разделитель
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet('background-color: #bdc3c7; margin: 10px 0;')
        main_layout.addWidget(line)
        
        main_layout.addSpacing(10)
        
        # Поле логина
        username_label = QLabel('📧 Логин:')
        username_label.setStyleSheet('font-size: 12pt; font-weight: 600; color: #34495e;')
        main_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите логин (admin)')
        self.username_input.setMinimumHeight(45)
        main_layout.addWidget(self.username_input)
        
        main_layout.addSpacing(8)
        
        # Поле пароля
        password_label = QLabel('🔒 Пароль:')
        password_label.setStyleSheet('font-size: 12pt; font-weight: 600; color: #34495e;')
        main_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.returnPressed.connect(self.login)
        main_layout.addWidget(self.password_input)
        
        main_layout.addSpacing(12)
        
        # Подсказка с учетными записями
        hint_label = QLabel('''
            <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid #ffc107;">
                <b>💡 Учетные записи для входа:</b><br>
                • <b>admin</b> / admin123 (полные права)<br>
                • <b>editor</b> / editor123 (редактирование)<br>
                • <b>user</b> / user123 (только просмотр)
            </div>
        ''')
        hint_label.setWordWrap(True)
        main_layout.addWidget(hint_label)
        
        main_layout.addSpacing(15)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.login_button = QPushButton('🔑 Войти в систему')
        self.login_button.setMinimumHeight(50)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.login)
        self.login_button.setDefault(True)
        
        cancel_button = QPushButton('✖ Отмена')
        cancel_button.setMinimumHeight(50)
        cancel_button.setMinimumWidth(120)
        cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.login_button, 2)
        button_layout.addWidget(cancel_button, 1)
        
        main_layout.addLayout(button_layout)
        
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(container)
        self.setLayout(wrapper_layout)
        
        # Фокус на поле логина
        self.username_input.setFocus()
        
        # Анимация появления
        self.fade_in_animation()
    
    def fade_in_animation(self):
        """Плавное появление окна"""
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(500)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        
        self.fade_animation = animation
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            
            QFrame#container {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-radius: 20px;
                border: 2px solid #e0e0e0;
            }
            
            QPushButton#closeButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 17px;
                font-size: 16pt;
                font-weight: bold;
            }
            
            QPushButton#closeButton:hover {
                background-color: #d32f2f;
            }
            
            QPushButton#closeButton:pressed {
                background-color: #b71c1c;
            }
            
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 12px 18px;
                font-size: 12pt;
                background-color: white;
                selection-background-color: #2196f3;
            }
            
            QLineEdit:focus {
                border: 2px solid #2196f3;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #e3f2fd);
            }
            
            QLineEdit:hover {
                border: 2px solid #90caf9;
                background-color: #fafafa;
            }
            
            QPushButton {
                border: none;
                border-radius: 12px;
                padding: 14px 28px;
                font-size: 12pt;
                font-weight: 700;
                letter-spacing: 0.8px;
            }
            
            QPushButton:default {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196f3, stop:0.5 #1976d2, stop:1 #1565c0);
                color: white;
                border: none;
            }
            
            QPushButton:default:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1976d2, stop:0.5 #1565c0, stop:1 #0d47a1);
            }
            
            QPushButton:default:pressed {
                background: #0d47a1;
                padding: 15px 27px 13px 29px;
            }
            
            QPushButton:!default {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #757575, stop:1 #616161);
                color: white;
            }
            
            QPushButton:!default:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #616161, stop:1 #424242);
            }
            
            QPushButton:!default:pressed {
                background: #424242;
                padding: 15px 27px 13px 29px;
            }
        """)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(
                self, 
                '⚠️ Ошибка', 
                'Пожалуйста, заполните все поля!'
            )
            return
        
        if self.auth_manager.authenticate(username, password):
            self.accept()
        else:
            QMessageBox.critical(
                self, 
                '❌ Ошибка входа', 
                '<b>Неверный логин или пароль!</b><br><br>'
                'Попробуйте:<br>'
                '• <b>admin</b> / admin123<br>'
                '• <b>editor</b> / editor123<br>'
                '• <b>user</b> / user123'
            )
            self.password_input.clear()
            self.password_input.setFocus()

"""
Современные виджеты с анимациями и эффектами
"""
from PyQt6.QtWidgets import (QPushButton, QLabel, QFrame, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QLineEdit)
from PyQt6.QtCore import (Qt, QPropertyAnimation, QEasingCurve, QSize, 
                          pyqtProperty, QRect, QPoint)
from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QFont, QPen, QBrush, QPixmap


class AnimatedButton(QPushButton):
    """Кнопка с анимацией при наведении"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scale = 1.0
        
        # Тень
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        # Стили
        self.setStyleSheet("""
            AnimatedButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196f3, stop:1 #1976d2);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            AnimatedButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1976d2, stop:1 #1565c0);
            }
            AnimatedButton:pressed {
                background: #0d47a1;
            }
        """)
    
    def enterEvent(self, event):
        """Анимация при наведении"""
        self.animation = QPropertyAnimation(self, b"scale")
        self.animation.setDuration(200)
        self.animation.setStartValue(self._scale)
        self.animation.setEndValue(1.05)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Анимация при уходе"""
        self.animation = QPropertyAnimation(self, b"scale")
        self.animation.setDuration(200)
        self.animation.setStartValue(self._scale)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        super().leaveEvent(event)
    
    def get_scale(self):
        return self._scale
    
    def set_scale(self, value):
        self._scale = value
        self.update()
    
    scale = pyqtProperty(float, get_scale, set_scale)


class ModernCard(QFrame):
    """Современная карточка с тенью и hover эффектом"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self._hover = False
        
        # Тень
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            ModernCard {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }
            ModernCard:hover {
                border: 1px solid #2196f3;
            }
        """)
    
    def enterEvent(self, event):
        """Анимация при наведении"""
        self._hover = True
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            # Увеличиваем тень
            self.shadow_animation = QPropertyAnimation(effect, b"blurRadius")
            self.shadow_animation.setDuration(200)
            self.shadow_animation.setStartValue(20)
            self.shadow_animation.setEndValue(30)
            self.shadow_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.shadow_animation.start()
            
            self.offset_animation = QPropertyAnimation(effect, b"offset")
            self.offset_animation.setDuration(200)
            self.offset_animation.setStartValue(QPoint(0, 4))
            self.offset_animation.setEndValue(QPoint(0, 8))
            self.offset_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.offset_animation.start()
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Анимация при уходе"""
        self._hover = False
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            # Уменьшаем тень
            self.shadow_animation = QPropertyAnimation(effect, b"blurRadius")
            self.shadow_animation.setDuration(200)
            self.shadow_animation.setStartValue(30)
            self.shadow_animation.setEndValue(20)
            self.shadow_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.shadow_animation.start()
            
            self.offset_animation = QPropertyAnimation(effect, b"offset")
            self.offset_animation.setDuration(200)
            self.offset_animation.setStartValue(QPoint(0, 8))
            self.offset_animation.setEndValue(QPoint(0, 4))
            self.offset_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.offset_animation.start()
        
        super().leaveEvent(event)


class GradientLabel(QLabel):
    """Label с градиентным фоном"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Градиентный фон
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(33, 150, 243))
        gradient.setColorAt(1, QColor(25, 118, 210))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        
        # Текст
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())


class ModernSearchBox(QLineEdit):
    """Современное поле поиска"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("🔍 Поиск...")
        self.setMinimumHeight(45)
        
        # Тень
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            ModernSearchBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 22px;
                padding: 8px 20px;
                font-size: 11pt;
                color: #212529;
            }
            ModernSearchBox:focus {
                border: 2px solid #2196f3;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
            }
            ModernSearchBox:hover {
                border: 2px solid #90caf9;
            }
        """)


class StatsCard(QFrame):
    """Карточка статистики с иконкой"""
    def __init__(self, icon, title, value, color="#2196f3", parent=None):
        super().__init__(parent)
        self.icon = icon
        self.title = title
        self.value = value
        self.color = color
        
        self.setMinimumSize(200, 120)
        self.setMaximumSize(300, 120)
        
        # Тень
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setStyleSheet(f"""
            StatsCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.color}, stop:1 {self.adjust_color(self.color, -20)});
                border-radius: 16px;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Иконка
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("font-size: 32pt; color: white;")
        layout.addWidget(icon_label)
        
        # Значение
        value_label = QLabel(str(self.value))
        value_label.setStyleSheet("""
            font-size: 28pt;
            font-weight: bold;
            color: white;
        """)
        layout.addWidget(value_label)
        
        # Название
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-size: 10pt;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        """)
        layout.addWidget(title_label)
        
        layout.addStretch()
    
    def adjust_color(self, hex_color, amount):
        """Изменение яркости цвета"""
        # Простое изменение цвета
        color = QColor(hex_color)
        h, s, l, a = color.getHsl()
        l = max(0, min(255, l + amount))
        color.setHsl(h, s, l, a)
        return color.name()


class EmployeeCardWidget(ModernCard):
    """Красивая карточка сотрудника"""
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.employee_data = employee_data
        self.setMinimumSize(300, 180)
        self.setMaximumHeight(200)
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса карточки"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Аватар
        avatar_label = QLabel()
        avatar_label.setFixedSize(80, 80)
        avatar_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2196f3, stop:1 #1976d2);
                border-radius: 40px;
                color: white;
                font-size: 32pt;
                border: 3px solid #e3f2fd;
            }
        """)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setText("👤")
        layout.addWidget(avatar_label)
        
        # Информация
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        # Имя
        name_label = QLabel(self.employee_data.get('name', 'Сотрудник'))
        name_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #212529;
        """)
        info_layout.addWidget(name_label)
        
        # Должность
        position_label = QLabel(self.employee_data.get('position', 'Должность'))
        position_label.setStyleSheet("""
            font-size: 10pt;
            color: #6c757d;
            font-weight: 500;
        """)
        info_layout.addWidget(position_label)
        
        # Отдел
        dept_label = QLabel(f"📁 {self.employee_data.get('department', 'Отдел')}")
        dept_label.setStyleSheet("""
            font-size: 9pt;
            color: #2196f3;
            font-weight: 500;
            padding: 4px 8px;
            background-color: #e3f2fd;
            border-radius: 8px;
        """)
        dept_label.setMaximumWidth(200)
        info_layout.addWidget(dept_label)
        
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
        layout.addStretch()


class IconButton(QPushButton):
    """Круглая кнопка с иконкой"""
    def __init__(self, icon_text, tooltip="", parent=None):
        super().__init__(icon_text, parent)
        self.setFixedSize(50, 50)
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Тень
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            IconButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2196f3, stop:1 #1976d2);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18pt;
            }
            IconButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1976d2, stop:1 #1565c0);
            }
            IconButton:pressed {
                background: #0d47a1;
            }
        """)


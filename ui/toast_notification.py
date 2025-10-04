from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont

class ToastNotification(QLabel):
    def __init__(self, parent, message: str, toast_type: str = "info"):
        super().__init__(parent)
        self.parent_widget = parent
        self.setup_ui(message, toast_type)
        
    def setup_ui(self, message: str, toast_type: str):
        self.setText(message)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        
        colors = {
            "success": "#27ae60",
            "error": "#e74c3c",
            "warning": "#f39c12",
            "info": "#3498db"
        }
        
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        bg_color = colors.get(toast_type, colors["info"])
        icon = icons.get(toast_type, icons["info"])
        
        self.setText(f"{icon} {message}")
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                padding: 15px 25px;
                border-radius: 10px;
                font-size: 12pt;
                font-weight: 600;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)
        
        self.adjustSize()
        self.raise_()
        
    def show_toast(self, duration: int = 3000):
        parent_rect = self.parent_widget.rect()
        x = (parent_rect.width() - self.width()) // 2
        y = parent_rect.height() - self.height() - 50
        
        self.move(x, parent_rect.height())
        self.show()
        
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setStartValue(QPoint(x, parent_rect.height()))
        self.animation.setEndValue(QPoint(x, y))
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        
        QTimer.singleShot(duration, self.hide_toast)
    
    def hide_toast(self):
        parent_rect = self.parent_widget.rect()
        x = self.x()
        
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(x, parent_rect.height()))
        self.animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()

def show_toast(parent, message: str, toast_type: str = "info", duration: int = 3000):
    toast = ToastNotification(parent, message, toast_type)
    toast.show_toast(duration)
    return toast




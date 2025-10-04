"""
Анимированная заставка при запуске приложения
"""
from PyQt6.QtWidgets import QSplashScreen, QLabel, QProgressBar, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QFont, QPen, QBrush, QRadialGradient

class ModernSplashScreen(QSplashScreen):
    def __init__(self):
        # Создаем пустой pixmap для splash screen
        pixmap = QPixmap(600, 400)
        pixmap.fill(Qt.GlobalColor.transparent)
        super().__init__(pixmap)
        
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.SplashScreen
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Переменные анимации
        self.progress = 0
        self.logo_scale = 0.0
        self.opacity = 0.0
        
        # Таймеры
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(20)  # 50 FPS
        
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(30)
        
        self.messages = [
            "Инициализация модулей...",
            "Загрузка базы данных...",
            "Подготовка интерфейса...",
            "Настройка компонентов...",
            "Проверка подключений...",
            "Финализация запуска..."
        ]
        self.current_message_idx = 0
        self.current_message = self.messages[0]
    
    def update_animation(self):
        """Обновление анимации"""
        # Плавное увеличение логотипа
        if self.logo_scale < 1.0:
            self.logo_scale += 0.02
        
        # Плавное появление
        if self.opacity < 1.0:
            self.opacity += 0.03
        
        self.update()
    
    def update_progress(self):
        """Обновление прогресса"""
        if self.progress < 100:
            self.progress += 2
            
            # Обновление сообщения
            new_idx = int((self.progress / 100) * len(self.messages))
            if new_idx != self.current_message_idx and new_idx < len(self.messages):
                self.current_message_idx = new_idx
                self.current_message = self.messages[new_idx]
        else:
            self.progress_timer.stop()
            # Плавное закрытие
            QTimer.singleShot(300, self.close)
    
    def drawContents(self, painter: QPainter):
        """Отрисовка содержимого splash screen"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        width = self.width()
        height = self.height()
        
        # Применяем прозрачность
        painter.setOpacity(self.opacity)
        
        # Фон с градиентом
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(25, 118, 210))  # #1976D2
        gradient.setColorAt(0.5, QColor(33, 150, 243))  # #2196F3
        gradient.setColorAt(1, QColor(25, 118, 210))
        
        # Рисуем закругленный прямоугольник
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, width, height, 20, 20)
        
        # Рисуем декоративные круги на фоне
        painter.setOpacity(0.1 * self.opacity)
        radial1 = QRadialGradient(width * 0.2, height * 0.3, 150)
        radial1.setColorAt(0, QColor(255, 255, 255, 100))
        radial1.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(radial1))
        painter.drawEllipse(int(width * 0.2 - 75), int(height * 0.3 - 75), 150, 150)
        
        radial2 = QRadialGradient(width * 0.8, height * 0.7, 120)
        radial2.setColorAt(0, QColor(255, 255, 255, 80))
        radial2.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(radial2))
        painter.drawEllipse(int(width * 0.8 - 60), int(height * 0.7 - 60), 120, 120)
        
        painter.setOpacity(self.opacity)
        
        # Логотип (emoji) с анимацией масштабирования
        center_x = width // 2
        center_y = height // 2 - 50
        
        painter.save()
        painter.translate(center_x, center_y)
        painter.scale(self.logo_scale, self.logo_scale)
        
        # Рисуем круг для логотипа
        painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
        painter.setPen(QPen(QColor(255, 255, 255, 100), 3))
        painter.drawEllipse(-60, -60, 120, 120)
        
        # Emoji логотип
        font = QFont("Segoe UI Emoji", 60)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(-35, 20, "👥")
        
        painter.restore()
        
        # Название приложения
        title_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.setPen(QColor(255, 255, 255))
        title_text = "Employee Directory"
        title_metrics = painter.fontMetrics()
        title_width = title_metrics.horizontalAdvance(title_text)
        painter.drawText((width - title_width) // 2, center_y + 80, title_text)
        
        # Версия
        version_font = QFont("Segoe UI", 11)
        painter.setFont(version_font)
        painter.setPen(QColor(255, 255, 255, 200))
        version_text = "Employee Directory"
        version_metrics = painter.fontMetrics()
        version_width = version_metrics.horizontalAdvance(version_text)
        painter.drawText((width - version_width) // 2, center_y + 105, version_text)
        
        # Прогресс бар
        progress_y = height - 80
        progress_width = width - 80
        progress_x = 40
        progress_height = 8
        
        # Фон прогресс бара
        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(progress_x, progress_y, progress_width, progress_height, 4, 4)
        
        # Заполненная часть прогресс бара
        filled_width = int((self.progress / 100) * progress_width)
        
        progress_gradient = QLinearGradient(progress_x, 0, progress_x + filled_width, 0)
        progress_gradient.setColorAt(0, QColor(255, 255, 255))
        progress_gradient.setColorAt(1, QColor(200, 230, 255))
        
        painter.setBrush(QBrush(progress_gradient))
        painter.drawRoundedRect(progress_x, progress_y, filled_width, progress_height, 4, 4)
        
        # Текст прогресса
        status_font = QFont("Segoe UI", 9)
        painter.setFont(status_font)
        painter.setPen(QColor(255, 255, 255, 230))
        painter.drawText(progress_x, progress_y + 25, f"{self.current_message}")
        
        # Процент справа
        percent_text = f"{self.progress}%"
        percent_metrics = painter.fontMetrics()
        percent_width = percent_metrics.horizontalAdvance(percent_text)
        painter.drawText(progress_x + progress_width - percent_width, progress_y + 25, percent_text)
        
        # Тень по краям для глубины
        painter.setOpacity(0.3 * self.opacity)
        shadow_gradient = QLinearGradient(0, 0, 0, 20)
        shadow_gradient.setColorAt(0, QColor(0, 0, 0, 50))
        shadow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(shadow_gradient))
        painter.drawRoundedRect(0, 0, width, 20, 20, 20)
        
        painter.setOpacity(self.opacity)


class SimpleSplashScreen(QWidget):
    """Упрощенная версия заставки для быстрой загрузки"""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.SplashScreen
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(600, 400)
        
        # Центрируем на экране
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
        
        self.progress = 0
        self.setup_ui()
        
        # Таймер прогресса
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)
    
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1976d2, stop:0.5 #2196f3, stop:1 #1976d2);
                border-radius: 20px;
            }
        """)
    
    def update_progress(self):
        """Обновление прогресса"""
        if self.progress < 100:
            self.progress += 3
            self.update()
        else:
            self.timer.stop()
            QTimer.singleShot(200, self.close)
    
    def paintEvent(self, event):
        """Отрисовка"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Логотип
        font = QFont("Segoe UI Emoji", 70)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(width // 2 - 40, height // 2 - 20, "👥")
        
        # Название
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.drawText(0, height // 2 + 60, width, 30, 
                        Qt.AlignmentFlag.AlignCenter, "Employee Directory")
        
        # Прогресс бар
        progress_y = height - 60
        progress_width = width - 80
        progress_x = 40
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.drawRoundedRect(progress_x, progress_y, progress_width, 6, 3, 3)
        
        filled_width = int((self.progress / 100) * progress_width)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRoundedRect(progress_x, progress_y, filled_width, 6, 3, 3)


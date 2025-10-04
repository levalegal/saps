from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QColor, QPen

class DragDropImportWidget(QWidget):
    files_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.is_dragging = False
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("📂\nПеретащите сюда файлы CSV или Excel\nдля импорта сотрудников")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12pt;
                padding: 40px;
                border: 3px dashed #bdc3c7;
                border-radius: 15px;
                background-color: #ecf0f1;
            }
        """)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.csv', '.xlsx', '.xls')):
                    event.acceptProposedAction()
                    self.is_dragging = True
                    self.label.setStyleSheet("""
                        QLabel {
                            color: #27ae60;
                            font-size: 12pt;
                            padding: 40px;
                            border: 3px dashed #27ae60;
                            border-radius: 15px;
                            background-color: #d5f4e6;
                        }
                    """)
                    return
    
    def dragLeaveEvent(self, event):
        self.is_dragging = False
        self.label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12pt;
                padding: 40px;
                border: 3px dashed #bdc3c7;
                border-radius: 15px;
                background-color: #ecf0f1;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.csv', '.xlsx', '.xls')):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)
        
        self.is_dragging = False
        self.label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12pt;
                padding: 40px;
                border: 3px dashed #bdc3c7;
                border-radius: 15px;
                background-color: #ecf0f1;
            }
        """)




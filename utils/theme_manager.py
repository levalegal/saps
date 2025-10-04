class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
    
    def set_theme(self, theme: str):
        self.current_theme = theme
    
    def get_light_theme(self) -> str:
        return """
            QMainWindow {
                background-color: #f5f6fa;
            }
            
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f0f0);
                border: none;
                border-bottom: 2px solid #e1e8ed;
                padding: 8px;
                spacing: 5px;
            }
            
            QToolBar QToolButton {
                background-color: transparent;
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 8px 12px;
                margin: 2px;
                font-size: 11pt;
                font-weight: 500;
                color: #2c3e50;
            }
            
            QToolBar QToolButton:hover {
                background-color: #e3f2fd;
                border: 2px solid #90caf9;
            }
            
            QToolBar QToolButton:pressed {
                background-color: #bbdefb;
            }
            
            QMenuBar {
                background-color: #2c3e50;
                color: white;
                padding: 5px;
                font-size: 10pt;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 15px;
                border-radius: 5px;
            }
            
            QMenuBar::item:selected {
                background-color: #34495e;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 5px;
            }
            
            QMenu::item {
                padding: 8px 25px 8px 15px;
                border-radius: 5px;
                color: #2c3e50;
            }
            
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f0f0, stop:1 #ffffff);
                border-top: 2px solid #e1e8ed;
                color: #2c3e50;
                font-size: 10pt;
                padding: 5px;
            }
            
            #centerPanel {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
            
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e1e8ed;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                selection-background-color: #3498db;
                selection-color: white;
                font-size: 10pt;
                color: #2c3e50;
            }
            
            QTableWidget::item {
                padding: 8px;
            }
            
            QTableWidget::item:hover {
                background-color: #e3f2fd;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 10px;
                border: none;
                border-right: 1px solid #2874a6;
                font-weight: bold;
                font-size: 10pt;
            }
            
            QHeaderView::section:hover {
                background: #2874a6;
            }
            
            QTreeWidget {
                background-color: white;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 10pt;
                padding: 5px;
                color: #2c3e50;
            }
            
            QTreeWidget::item {
                padding: 8px;
                border-radius: 5px;
            }
            
            QTreeWidget::item:hover {
                background-color: #e3f2fd;
            }
            
            QTreeWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 10pt;
                background-color: white;
                color: #2c3e50;
            }
            
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #f8f9fa;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
            }
            
            QPushButton:pressed {
                background: #1a5276;
            }
            
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 10pt;
                background-color: white;
                color: #2c3e50;
            }
            
            QComboBox:hover {
                border: 2px solid #3498db;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QLabel {
                color: #2c3e50;
                font-size: 10pt;
            }
            
            QGroupBox {
                background-color: white;
                border: 2px solid #e1e8ed;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: bold;
                font-size: 11pt;
                color: #2c3e50;
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
        """
    
    def get_dark_theme(self) -> str:
        return """
            QMainWindow {
                background-color: #1e1e1e;
            }
            
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d30, stop:1 #252526);
                border: none;
                border-bottom: 2px solid #3e3e42;
                padding: 8px;
                spacing: 5px;
            }
            
            QToolBar QToolButton {
                background-color: transparent;
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 8px 12px;
                margin: 2px;
                font-size: 11pt;
                font-weight: 500;
                color: #cccccc;
            }
            
            QToolBar QToolButton:hover {
                background-color: #3e3e42;
                border: 2px solid #007acc;
            }
            
            QToolBar QToolButton:pressed {
                background-color: #094771;
            }
            
            QMenuBar {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 5px;
                font-size: 10pt;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 15px;
                border-radius: 5px;
            }
            
            QMenuBar::item:selected {
                background-color: #3e3e42;
            }
            
            QMenu {
                background-color: #252526;
                border: 1px solid #3e3e42;
                border-radius: 8px;
                padding: 5px;
                color: #cccccc;
            }
            
            QMenu::item {
                padding: 8px 25px 8px 15px;
                border-radius: 5px;
            }
            
            QMenu::item:selected {
                background-color: #094771;
                color: white;
            }
            
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #252526, stop:1 #2d2d30);
                border-top: 2px solid #3e3e42;
                color: #cccccc;
                font-size: 10pt;
                padding: 5px;
            }
            
            #centerPanel {
                background-color: #252526;
                border-radius: 10px;
                padding: 10px;
            }
            
            QTableWidget {
                background-color: #252526;
                alternate-background-color: #2d2d30;
                gridline-color: #3e3e42;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                selection-background-color: #094771;
                selection-color: white;
                font-size: 10pt;
                color: #cccccc;
            }
            
            QTableWidget::item {
                padding: 8px;
            }
            
            QTableWidget::item:hover {
                background-color: #3e3e42;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #094771, stop:1 #007acc);
                color: white;
                padding: 10px;
                border: none;
                border-right: 1px solid #005a9e;
                font-weight: bold;
                font-size: 10pt;
            }
            
            QHeaderView::section:hover {
                background: #005a9e;
            }
            
            QTreeWidget {
                background-color: #252526;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                font-size: 10pt;
                padding: 5px;
                color: #cccccc;
            }
            
            QTreeWidget::item {
                padding: 8px;
                border-radius: 5px;
            }
            
            QTreeWidget::item:hover {
                background-color: #3e3e42;
            }
            
            QTreeWidget::item:selected {
                background-color: #094771;
                color: white;
            }
            
            QLineEdit {
                border: 2px solid #3e3e42;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 10pt;
                background-color: #1e1e1e;
                color: #cccccc;
            }
            
            QLineEdit:focus {
                border: 2px solid #007acc;
                background-color: #252526;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0e639c, stop:1 #007acc);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1177bb, stop:1 #1c91d4);
            }
            
            QPushButton:pressed {
                background: #005a9e;
            }
            
            QPushButton:disabled {
                background-color: #3e3e42;
                color: #6d6d6d;
            }
            
            QComboBox {
                border: 2px solid #3e3e42;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 10pt;
                background-color: #1e1e1e;
                color: #cccccc;
            }
            
            QComboBox:hover {
                border: 2px solid #007acc;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #252526;
                color: #cccccc;
                selection-background-color: #094771;
            }
            
            QLabel {
                color: #cccccc;
                font-size: 10pt;
            }
            
            QGroupBox {
                background-color: #252526;
                border: 2px solid #3e3e42;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: bold;
                font-size: 11pt;
                color: #cccccc;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
                background-color: #007acc;
                color: white;
                border-radius: 5px;
                margin-left: 10px;
            }
            
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 2px solid #3e3e42;
                border-radius: 8px;
            }
            
            QTextEdit:focus {
                border: 2px solid #007acc;
            }
            
            QDateEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                padding: 8px;
            }
            
            QDateEdit:focus {
                border: 2px solid #007acc;
            }
            
            QCheckBox {
                color: #cccccc;
            }
            
            QScrollBar:vertical {
                background-color: #1e1e1e;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #3e3e42;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #4e4e52;
            }
            
            QScrollBar:horizontal {
                background-color: #1e1e1e;
                height: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #3e3e42;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #4e4e52;
            }
        """
    
    def get_current_theme_stylesheet(self) -> str:
        if self.current_theme == "dark":
            return self.get_dark_theme()
        else:
            return self.get_light_theme()




from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QComboBox,
                             QLineEdit, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from utils.activity_logger import ActivityLogger
from datetime import datetime

class HistoryDialog(QDialog):
    def __init__(self, logger: ActivityLogger, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        self.setWindowTitle('📜 История изменений')
        self.setMinimumSize(900, 600)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e1e8ed;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
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
            QComboBox, QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel('📜 История изменений')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3498db, stop:1 #2980b9);
            color: white;
            padding: 12px;
            border-radius: 8px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        filter_layout = QHBoxLayout()
        
        self.action_filter = QComboBox()
        self.action_filter.addItem('Все действия', None)
        self.action_filter.addItems(['ДОБАВЛЕН', 'ОБНОВЛЕН', 'УДАЛЕН', 'ЭКСПОРТ', 'ИМПОРТ', 'ПОИСК', 'ВХОД'])
        self.action_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel('Действие:'))
        filter_layout.addWidget(self.action_filter)
        
        self.type_filter = QComboBox()
        self.type_filter.addItem('Все типы', None)
        self.type_filter.addItems(['Сотрудник', 'Отдел', 'Система'])
        self.type_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel('Тип:'))
        filter_layout.addWidget(self.type_filter)
        
        self.user_filter = QLineEdit()
        self.user_filter.setPlaceholderText('Фильтр по пользователю...')
        self.user_filter.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel('Пользователь:'))
        filter_layout.addWidget(self.user_filter)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            '🕐 Время',
            '🎯 Действие',
            '📋 Тип',
            '🔢 ID',
            '👤 Пользователь',
            '📝 Детали'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
        
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton('🔄 Обновить')
        refresh_button.clicked.connect(self.load_history)
        button_layout.addWidget(refresh_button)
        
        export_button = QPushButton('📥 Экспорт в CSV')
        export_button.clicked.connect(self.export_history)
        button_layout.addWidget(export_button)
        
        button_layout.addStretch()
        
        close_button = QPushButton('❌ Закрыть')
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_history(self, limit=200):
        self.all_history = self.logger.get_recent_history(limit)
        self.apply_filters()
    
    def apply_filters(self):
        filtered_history = self.all_history
        
        action = self.action_filter.currentText()
        if action != 'Все действия':
            filtered_history = [h for h in filtered_history if h['action'] == action]
        
        entity_type = self.type_filter.currentText()
        if entity_type != 'Все типы':
            filtered_history = [h for h in filtered_history if h['entity_type'] == entity_type]
        
        user = self.user_filter.text().strip().lower()
        if user:
            filtered_history = [h for h in filtered_history if user in h['user'].lower()]
        
        self.display_history(filtered_history)
    
    def display_history(self, history):
        self.table.setRowCount(len(history))
        
        for row, entry in enumerate(history):
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            
            self.table.setItem(row, 0, QTableWidgetItem(timestamp))
            
            action_item = QTableWidgetItem(entry['action'])
            if entry['action'] == 'ДОБАВЛЕН':
                action_item.setForeground(Qt.GlobalColor.darkGreen)
            elif entry['action'] == 'УДАЛЕН':
                action_item.setForeground(Qt.GlobalColor.red)
            elif entry['action'] == 'ОБНОВЛЕН':
                action_item.setForeground(Qt.GlobalColor.blue)
            self.table.setItem(row, 1, action_item)
            
            self.table.setItem(row, 2, QTableWidgetItem(entry['entity_type']))
            self.table.setItem(row, 3, QTableWidgetItem(str(entry['entity_id']) if entry['entity_id'] else '-'))
            self.table.setItem(row, 4, QTableWidgetItem(entry['user']))
            self.table.setItem(row, 5, QTableWidgetItem(entry['details'] or '-'))
    
    def export_history(self):
        from PyQt6.QtWidgets import QFileDialog
        import csv
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Экспорт истории',
            'history_export.csv',
            'CSV Files (*.csv)'
        )
        
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Время', 'Действие', 'Тип', 'ID', 'Пользователь', 'Детали'])
                
                for entry in self.all_history:
                    timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([
                        timestamp,
                        entry['action'],
                        entry['entity_type'],
                        entry['entity_id'] or '-',
                        entry['user'],
                        entry['details'] or '-'
                    ])
            
            from ui.toast_notification import show_toast
            show_toast(self, f'История экспортирована: {filename}', 'success')




from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QDateEdit,
                             QFormLayout, QCheckBox, QTabWidget, QWidget,
                             QScrollArea, QFrame, QListWidget, QListWidgetItem)
from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from database.database import Database
import json
import os

class FilterTagWidget(QWidget):
    remove_clicked = pyqtSignal(str)
    
    def __init__(self, text: str, filter_key: str):
        super().__init__()
        self.filter_key = filter_key
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #3498db;
                border-radius: 12px;
                padding: 2px;
            }
        """)
        
        label = QLabel(text)
        label.setStyleSheet("color: white; padding: 5px 10px; font-size: 9pt;")
        layout.addWidget(label)
        
        remove_btn = QPushButton("✕")
        remove_btn.setFixedSize(20, 20)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_clicked.emit(self.filter_key))
        layout.addWidget(remove_btn)
        
        self.setLayout(layout)
        self.setMaximumHeight(30)

class ModernAdvancedSearchDialog(QDialog):
    def __init__(self, database: Database, parent=None):
        super().__init__(parent)
        self.database = database
        self.search_criteria = {}
        self.saved_filters_file = 'saved_filters.json'
        self.init_ui()
        self.load_saved_filters()
    
    def init_ui(self):
        self.setWindowTitle('🔎 Расширенный поиск')
        self.setMinimumSize(650, 550)
        
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
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 10pt;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #3498db;
                border: 2px solid #e1e8ed;
                border-bottom: 2px solid white;
            }
            QLineEdit, QComboBox, QDateEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #3498db;
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
            QPushButton#clearButton {
                background-color: #95a5a6;
            }
            QPushButton#clearButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton#cancelButton {
                background-color: #e74c3c;
            }
            QPushButton#cancelButton:hover {
                background-color: #c0392b;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel('🔎 Расширенный поиск')
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
        main_layout.addWidget(title_label)
        
        self.tags_layout = QHBoxLayout()
        self.tags_layout.setSpacing(8)
        self.tags_layout.addStretch()
        main_layout.addLayout(self.tags_layout)
        
        tabs = QTabWidget()
        
        basic_tab = self.create_basic_tab()
        tabs.addTab(basic_tab, "🔍 Основные критерии")
        
        additional_tab = self.create_additional_tab()
        tabs.addTab(additional_tab, "⚙️ Дополнительные")
        
        saved_tab = self.create_saved_filters_tab()
        tabs.addTab(saved_tab, "💾 Сохраненные")
        
        main_layout.addWidget(tabs)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_filter_button = QPushButton('💾 Сохранить фильтр')
        save_filter_button.clicked.connect(self.save_current_filter)
        button_layout.addWidget(save_filter_button)
        
        search_button = QPushButton('🔎 Найти')
        search_button.clicked.connect(self.accept)
        search_button.setMinimumWidth(120)
        button_layout.addWidget(search_button)
        
        clear_button = QPushButton('🗑️ Очистить')
        clear_button.setObjectName("clearButton")
        clear_button.clicked.connect(self.clear_fields)
        clear_button.setMinimumWidth(120)
        button_layout.addWidget(clear_button)
        
        cancel_button = QPushButton('❌ Отмена')
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumWidth(120)
        button_layout.addWidget(cancel_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def create_basic_tab(self):
        tab = QWidget()
        form_layout = QFormLayout()
        form_layout.setContentsMargins(30, 20, 30, 20)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.fio_input = QLineEdit()
        self.fio_input.setPlaceholderText('Введите ФИО...')
        form_layout.addRow('👤 ФИО:', self.fio_input)
        
        self.department_combo = QComboBox()
        self.department_combo.addItem('🏢 Любой', None)
        departments = self.database.get_all_departments()
        for dept in departments:
            self.department_combo.addItem(f"🏢 {dept.name}", dept.id)
        form_layout.addRow('🏢 Отдел:', self.department_combo)
        
        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText('Введите должность...')
        form_layout.addRow('💼 Должность:', self.position_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Введите email...')
        form_layout.addRow('📧 Email:', self.email_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Введите телефон...')
        form_layout.addRow('📞 Телефон:', self.phone_input)
        
        tab.setLayout(form_layout)
        return tab
    
    def create_additional_tab(self):
        tab = QWidget()
        form_layout = QFormLayout()
        form_layout.setContentsMargins(30, 20, 30, 20)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.skills_input = QLineEdit()
        self.skills_input.setPlaceholderText('Введите навыки...')
        form_layout.addRow('💼 Навыки:', self.skills_input)
        
        date_layout = QHBoxLayout()
        self.use_hire_date = QCheckBox()
        date_layout.addWidget(self.use_hire_date)
        
        self.hire_date_from = QDateEdit()
        self.hire_date_from.setCalendarPopup(True)
        self.hire_date_from.setDate(QDate.currentDate().addYears(-5))
        date_layout.addWidget(QLabel('С:'))
        date_layout.addWidget(self.hire_date_from)
        
        self.hire_date_to = QDateEdit()
        self.hire_date_to.setCalendarPopup(True)
        self.hire_date_to.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel('По:'))
        date_layout.addWidget(self.hire_date_to)
        
        form_layout.addRow('📅 Дата приема:', date_layout)
        
        self.has_photo = QCheckBox('📷 Только с фото')
        form_layout.addRow('', self.has_photo)
        
        tab.setLayout(form_layout)
        return tab
    
    def create_saved_filters_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        info_label = QLabel('💾 Сохраненные фильтры')
        info_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(info_label)
        
        self.saved_filters_list = QListWidget()
        self.saved_filters_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
        """)
        self.saved_filters_list.itemDoubleClicked.connect(self.load_selected_filter)
        layout.addWidget(self.saved_filters_list)
        
        btn_layout = QHBoxLayout()
        
        load_btn = QPushButton('📥 Загрузить')
        load_btn.clicked.connect(self.load_selected_filter)
        btn_layout.addWidget(load_btn)
        
        delete_btn = QPushButton('🗑️ Удалить')
        delete_btn.setObjectName("cancelButton")
        delete_btn.clicked.connect(self.delete_selected_filter)
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        
        tab.setLayout(layout)
        return tab
    
    def update_tags(self):
        while self.tags_layout.count() > 1:
            child = self.tags_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        criteria = self.get_search_criteria()
        
        if criteria:
            for key, value in criteria.items():
                if key == 'department_id':
                    dept = self.database.get_department(value)
                    tag = FilterTagWidget(f"Отдел: {dept.name if dept else value}", key)
                elif key == 'has_photo':
                    tag = FilterTagWidget("С фото", key)
                elif key == 'hire_date_from':
                    tag = FilterTagWidget(f"Прием: {value} - {criteria.get('hire_date_to', '')}", key)
                elif key == 'hire_date_to':
                    continue
                else:
                    tag = FilterTagWidget(f"{key}: {value}", key)
                
                tag.remove_clicked.connect(self.remove_tag)
                self.tags_layout.insertWidget(self.tags_layout.count() - 1, tag)
    
    def remove_tag(self, filter_key: str):
        if filter_key == 'fio':
            self.fio_input.clear()
        elif filter_key == 'department_id':
            self.department_combo.setCurrentIndex(0)
        elif filter_key == 'position':
            self.position_input.clear()
        elif filter_key == 'email':
            self.email_input.clear()
        elif filter_key == 'phone':
            self.phone_input.clear()
        elif filter_key == 'skills':
            self.skills_input.clear()
        elif filter_key == 'hire_date_from':
            self.use_hire_date.setChecked(False)
        elif filter_key == 'has_photo':
            self.has_photo.setChecked(False)
        
        self.update_tags()
    
    def clear_fields(self):
        self.fio_input.clear()
        self.department_combo.setCurrentIndex(0)
        self.position_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.skills_input.clear()
        self.use_hire_date.setChecked(False)
        self.has_photo.setChecked(False)
        self.update_tags()
    
    def get_search_criteria(self):
        criteria = {}
        
        if self.fio_input.text().strip():
            criteria['fio'] = self.fio_input.text().strip()
        
        if self.department_combo.currentData():
            criteria['department_id'] = self.department_combo.currentData()
        
        if self.position_input.text().strip():
            criteria['position'] = self.position_input.text().strip()
        
        if self.email_input.text().strip():
            criteria['email'] = self.email_input.text().strip()
        
        if self.phone_input.text().strip():
            criteria['phone'] = self.phone_input.text().strip()
        
        if self.skills_input.text().strip():
            criteria['skills'] = self.skills_input.text().strip()
        
        if self.use_hire_date.isChecked():
            criteria['hire_date_from'] = self.hire_date_from.date().toString('yyyy-MM-dd')
            criteria['hire_date_to'] = self.hire_date_to.date().toString('yyyy-MM-dd')
        
        if self.has_photo.isChecked():
            criteria['has_photo'] = True
        
        return criteria
    
    def save_current_filter(self):
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, 'Сохранить фильтр', 'Название фильтра:')
        if ok and name:
            criteria = self.get_search_criteria()
            if criteria:
                self.save_filter(name, criteria)
                from ui.toast_notification import show_toast
                show_toast(self, f'Фильтр "{name}" сохранен', 'success')
    
    def save_filter(self, name: str, criteria: dict):
        filters = {}
        if os.path.exists(self.saved_filters_file):
            with open(self.saved_filters_file, 'r', encoding='utf-8') as f:
                filters = json.load(f)
        
        filters[name] = criteria
        
        with open(self.saved_filters_file, 'w', encoding='utf-8') as f:
            json.dump(filters, f, ensure_ascii=False, indent=4)
        
        self.load_saved_filters()
    
    def load_saved_filters(self):
        self.saved_filters_list.clear()
        if os.path.exists(self.saved_filters_file):
            with open(self.saved_filters_file, 'r', encoding='utf-8') as f:
                filters = json.load(f)
                for name in filters.keys():
                    self.saved_filters_list.addItem(f"📁 {name}")
    
    def load_selected_filter(self):
        current_item = self.saved_filters_list.currentItem()
        if current_item:
            filter_name = current_item.text().replace("📁 ", "")
            
            with open(self.saved_filters_file, 'r', encoding='utf-8') as f:
                filters = json.load(f)
                criteria = filters.get(filter_name, {})
                
                self.clear_fields()
                
                if 'fio' in criteria:
                    self.fio_input.setText(criteria['fio'])
                if 'department_id' in criteria:
                    for i in range(self.department_combo.count()):
                        if self.department_combo.itemData(i) == criteria['department_id']:
                            self.department_combo.setCurrentIndex(i)
                            break
                if 'position' in criteria:
                    self.position_input.setText(criteria['position'])
                if 'email' in criteria:
                    self.email_input.setText(criteria['email'])
                if 'phone' in criteria:
                    self.phone_input.setText(criteria['phone'])
                if 'skills' in criteria:
                    self.skills_input.setText(criteria['skills'])
                if 'hire_date_from' in criteria:
                    self.use_hire_date.setChecked(True)
                    self.hire_date_from.setDate(QDate.fromString(criteria['hire_date_from'], 'yyyy-MM-dd'))
                    self.hire_date_to.setDate(QDate.fromString(criteria['hire_date_to'], 'yyyy-MM-dd'))
                if 'has_photo' in criteria:
                    self.has_photo.setChecked(criteria['has_photo'])
                
                self.update_tags()
                
                from ui.toast_notification import show_toast
                show_toast(self, f'Фильтр "{filter_name}" загружен', 'success')
    
    def delete_selected_filter(self):
        current_item = self.saved_filters_list.currentItem()
        if current_item:
            filter_name = current_item.text().replace("📁 ", "")
            
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self,
                'Подтверждение',
                f'Удалить фильтр "{filter_name}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                with open(self.saved_filters_file, 'r', encoding='utf-8') as f:
                    filters = json.load(f)
                
                if filter_name in filters:
                    del filters[filter_name]
                    
                    with open(self.saved_filters_file, 'w', encoding='utf-8') as f:
                        json.dump(filters, f, ensure_ascii=False, indent=4)
                    
                    self.load_saved_filters()
                    
                    from ui.toast_notification import show_toast
                    show_toast(self, f'Фильтр "{filter_name}" удален', 'warning')




from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
                             QTreeWidget, QTreeWidgetItem, QSplitter, QMessageBox,
                             QFileDialog, QLabel, QComboBox, QMenu, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QAction, QDesktopServices
from .modern_widgets import ModernSearchBox, IconButton, AnimatedButton, ModernCard
from .styles import get_main_stylesheet
from database.database import Database
from database.models import Employee
from auth.auth import AuthManager
from utils.export_import import ExportImport
from utils.qr_generator import QRGenerator
from utils.card_generator import CardGenerator
from utils.export_json import JSONExporter
from utils.backup_manager import BackupManager
from utils.settings_manager import SettingsManager
from database.cache import DataCache
from .dialogs import AddEditEmployeeDialog, AddDepartmentDialog
from .employee_card import EmployeeCard
from .statistics_widget import StatisticsWidget
from .advanced_search_dialog import AdvancedSearchDialog
from .settings_dialog import SettingsDialog
from .backup_dialog import BackupDialog
import webbrowser
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, database: Database, auth_manager: AuthManager):
        super().__init__()
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info("MainWindow: Initializing...")
            self.database = database
            self.auth_manager = auth_manager
            
            logger.info("MainWindow: Creating managers...")
            self.settings_manager = SettingsManager()
            self.backup_manager = BackupManager('employees.db')
            self.export_import = ExportImport(database)
            self.qr_generator = QRGenerator()
            self.card_generator = CardGenerator()
            self.json_exporter = JSONExporter()
            
            cache_ttl = self.settings_manager.get('cache_ttl', 300)
            self.cache = DataCache(ttl_seconds=cache_ttl)
            
            self.current_employees = []
            
            logger.info("MainWindow: Setting up UI...")
            self.init_ui()
            logger.info("MainWindow: Loading data...")
            self.load_data()
            logger.info("MainWindow: Checking birthdays...")
            self.check_birthdays()
            logger.info("MainWindow: Initialization complete!")
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            error_msg = f"MainWindow __init__ error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg, exc_info=True)
            raise
    
    def init_ui(self):
        self.setWindowTitle('👥 Employee Directory')
        self.setGeometry(100, 100, 1400, 850)
        
        self.create_menu_bar()
        self.create_toolbar()
        self.setup_shortcuts()
        self.apply_modern_styles()
        self.statusBar().showMessage('✅ Готов к работе • Нажмите F1 для справки')
        
        # Анимация появления окна
        self.fade_in_animation()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)
        
        right_panel = QSplitter(Qt.Orientation.Vertical)
        
        self.employee_card_widget = QWidget()
        self.employee_card_layout = QVBoxLayout()
        self.employee_card_widget.setLayout(self.employee_card_layout)
        right_panel.addWidget(self.employee_card_widget)
        
        self.statistics_widget = StatisticsWidget(self.database)
        self.statistics_widget.setMaximumHeight(300)
        right_panel.addWidget(self.statistics_widget)
        
        right_panel.setSizes([400, 300])
        splitter.addWidget(right_panel)
        
        splitter.setSizes([250, 600, 400])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        self.statusBar().showMessage('✅ Загрузка завершена')
    
    def fade_in_animation(self):
        """Плавное появление главного окна"""
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(600)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        
        self.window_animation = animation
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('Файл')
        
        import_action = QAction('Импорт из CSV', self)
        import_action.triggered.connect(self.import_csv)
        file_menu.addAction(import_action)
        
        import_excel_action = QAction('Импорт из Excel', self)
        import_excel_action.triggered.connect(self.import_excel)
        file_menu.addAction(import_excel_action)
        
        file_menu.addSeparator()
        
        export_csv_action = QAction('Экспорт в CSV', self)
        export_csv_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_csv_action)
        
        export_excel_action = QAction('Экспорт в Excel', self)
        export_excel_action.triggered.connect(self.export_excel)
        file_menu.addAction(export_excel_action)
        
        export_pdf_action = QAction('Экспорт в PDF', self)
        export_pdf_action.triggered.connect(self.export_pdf)
        file_menu.addAction(export_pdf_action)
        
        export_json_action = QAction('Экспорт в JSON', self)
        export_json_action.triggered.connect(self.export_json)
        file_menu.addAction(export_json_action)
        
        file_menu.addSeparator()
        
        export_selection_action = QAction('Экспорт текущей выборки...', self)
        export_selection_action.triggered.connect(self.export_current_selection)
        file_menu.addAction(export_selection_action)
        
        file_menu.addSeparator()
        
        export_card_action = QAction('Экспорт визитки (PNG)', self)
        export_card_action.triggered.connect(self.export_business_card)
        file_menu.addAction(export_card_action)
        
        export_sheet_action = QAction('Экспорт листа контактов (PNG)', self)
        export_sheet_action.triggered.connect(self.export_contact_sheet)
        file_menu.addAction(export_sheet_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        data_menu = menubar.addMenu('Данные')
        
        add_employee_action = QAction('Добавить сотрудника', self)
        add_employee_action.triggered.connect(self.add_employee)
        data_menu.addAction(add_employee_action)
        
        add_department_action = QAction('Добавить отдел', self)
        add_department_action.triggered.connect(self.add_department)
        data_menu.addAction(add_department_action)
        
        edit_employee_action = QAction('Редактировать сотрудника', self)
        edit_employee_action.triggered.connect(self.edit_employee)
        data_menu.addAction(edit_employee_action)
        
        delete_employee_action = QAction('Удалить сотрудника', self)
        delete_employee_action.triggered.connect(self.delete_employee)
        data_menu.addAction(delete_employee_action)
        
        duplicate_employee_action = QAction('Дублировать сотрудника', self)
        duplicate_employee_action.triggered.connect(self.duplicate_employee)
        data_menu.addAction(duplicate_employee_action)
        
        data_menu.addSeparator()
        
        delete_multiple_action = QAction('Массовое удаление', self)
        delete_multiple_action.triggered.connect(self.delete_multiple_employees)
        data_menu.addAction(delete_multiple_action)
        
        data_menu.addSeparator()
        
        advanced_search_action = QAction('Расширенный поиск...', self)
        advanced_search_action.triggered.connect(self.advanced_search)
        advanced_search_action.setShortcut('Ctrl+Shift+F')
        data_menu.addAction(advanced_search_action)
        
        tools_menu = menubar.addMenu('Инструменты')
        
        settings_action = QAction('Настройки...', self)
        settings_action.triggered.connect(self.show_settings)
        settings_action.setShortcut('Ctrl+,')
        tools_menu.addAction(settings_action)
        
        tools_menu.addSeparator()
        
        backup_action = QAction('Резервное копирование...', self)
        backup_action.triggered.connect(self.show_backup_dialog)
        tools_menu.addAction(backup_action)
        
        create_backup_action = QAction('Создать резервную копию', self)
        create_backup_action.triggered.connect(self.quick_backup)
        create_backup_action.setShortcut('Ctrl+B')
        tools_menu.addAction(create_backup_action)
        
        help_menu = menubar.addMenu('Справка')
        
        shortcuts_action = QAction('Горячие клавиши', self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        shortcuts_action.setShortcut('F1')
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        toolbar = self.addToolBar('Панель инструментов')
        toolbar.setMovable(False)
        toolbar.setIconSize(toolbar.iconSize() * 1.3)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        add_action = QAction('➕ Добавить', self)
        add_action.setToolTip('Добавить нового сотрудника (Ctrl+N)')
        add_action.triggered.connect(self.add_employee)
        toolbar.addAction(add_action)
        
        edit_action = QAction('✏️ Редактировать', self)
        edit_action.setToolTip('Редактировать выбранного сотрудника (Ctrl+E)')
        edit_action.triggered.connect(self.edit_employee)
        toolbar.addAction(edit_action)
        
        delete_action = QAction('🗑️ Удалить', self)
        delete_action.setToolTip('Удалить выбранного сотрудника (Del)')
        delete_action.triggered.connect(self.delete_employee)
        toolbar.addAction(delete_action)
        
        toolbar.addSeparator()
        
        refresh_action = QAction('🔄 Обновить', self)
        refresh_action.setToolTip('Обновить данные (F5)')
        refresh_action.triggered.connect(self.load_data)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        export_action = QAction('📤 Экспорт', self)
        export_action.setToolTip('Экспорт данных (Excel/CSV/PDF)')
        export_action.triggered.connect(self.show_export_menu)
        toolbar.addAction(export_action)
        
        toolbar.addSeparator()
        
        backup_action = QAction('💾 Бэкап', self)
        backup_action.setToolTip('Создать резервную копию (Ctrl+B)')
        backup_action.triggered.connect(self.quick_backup)
        toolbar.addAction(backup_action)
        
        settings_action = QAction('⚙️ Настройки', self)
        settings_action.setToolTip('Настройки приложения (Ctrl+,)')
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
    
    def setup_shortcuts(self):
        from PyQt6.QtGui import QShortcut, QKeySequence
        
        add_shortcut = QShortcut(QKeySequence('Ctrl+N'), self)
        add_shortcut.activated.connect(self.add_employee)
        
        edit_shortcut = QShortcut(QKeySequence('Ctrl+E'), self)
        edit_shortcut.activated.connect(self.edit_employee)
        
        delete_shortcut = QShortcut(QKeySequence('Del'), self)
        delete_shortcut.activated.connect(self.delete_employee)
        
        refresh_shortcut = QShortcut(QKeySequence('F5'), self)
        refresh_shortcut.activated.connect(self.refresh_data)
        
        search_shortcut = QShortcut(QKeySequence('Ctrl+F'), self)
        search_shortcut.activated.connect(self.focus_search)
    
    def create_left_panel(self):
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        dept_label = QLabel('🏢 Организационная структура')
        dept_label.setStyleSheet('''
            font-weight: bold; 
            font-size: 11pt; 
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3498db, stop:1 #2980b9);
            padding: 10px;
            border-radius: 8px;
        ''')
        dept_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(dept_label)
        
        self.department_tree = QTreeWidget()
        self.department_tree.setHeaderLabel('Структура организации')
        self.department_tree.itemClicked.connect(self.filter_by_department)
        left_layout.addWidget(self.department_tree)
        
        filter_label = QLabel('📋 Фильтр по должности:')
        filter_label.setStyleSheet('font-weight: 600; font-size: 10pt; color: #34495e; margin-top: 10px;')
        left_layout.addWidget(filter_label)
        
        self.position_filter = QComboBox()
        self.position_filter.addItem('Все должности', None)
        self.position_filter.currentIndexChanged.connect(self.apply_filters)
        left_layout.addWidget(self.position_filter)
        
        add_dept_button = QPushButton('➕ Добавить отдел')
        add_dept_button.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #229954, stop:1 #1e8449);
            }
        ''')
        add_dept_button.clicked.connect(self.add_department)
        left_layout.addWidget(add_dept_button)
        
        left_widget.setLayout(left_layout)
        return left_widget
    
    def create_center_panel(self):
        center_widget = QWidget()
        center_layout = QVBoxLayout()
        
        search_layout = QHBoxLayout()
        search_label = QLabel('🔍 Быстрый поиск:')
        search_label.setStyleSheet('font-weight: bold; font-size: 11pt; color: #2c3e50;')
        search_layout.addWidget(search_label)
        
        from PyQt6.QtWidgets import QCompleter
        from PyQt6.QtCore import QStringListModel
        
        self.search_input = ModernSearchBox()
        self.search_input.setPlaceholderText('🔍 Введите ФИО, должность, телефон или email...')
        self.search_input.textChanged.connect(self.search_employees)
        
        self.search_completer = QCompleter()
        self.search_completer_model = QStringListModel()
        self.search_completer.setModel(self.search_completer_model)
        self.search_input.setCompleter(self.search_completer)
        self.update_search_completer()
        
        search_layout.addWidget(self.search_input)
        
        advanced_search_button = QPushButton('🔎 Расширенный поиск')
        advanced_search_button.setToolTip('Открыть расширенный поиск (Ctrl+Shift+F)')
        advanced_search_button.clicked.connect(self.advanced_search)
        search_layout.addWidget(advanced_search_button)
        
        clear_button = QPushButton('✖ Очистить')
        clear_button.setStyleSheet('''
            QPushButton {
                background-color: #95a5a6;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        ''')
        clear_button.clicked.connect(self.clear_search)
        search_layout.addWidget(clear_button)
        
        center_layout.addLayout(search_layout)
        
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(6)
        self.employee_table.setHorizontalHeaderLabels([
            'ID', 'ФИО', 'Должность', 'Отдел', 'Телефон', 'Email'
        ])
        self.employee_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.employee_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.employee_table.setSortingEnabled(True)
        self.employee_table.itemSelectionChanged.connect(self.show_employee_card)
        self.employee_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.employee_table.customContextMenuRequested.connect(self.show_context_menu)
        self.employee_table.doubleClicked.connect(self.on_table_double_click)
        
        self.employee_table.setColumnWidth(0, 50)
        self.employee_table.setColumnWidth(1, 200)
        self.employee_table.setColumnWidth(2, 150)
        self.employee_table.setColumnWidth(3, 150)
        self.employee_table.setColumnWidth(4, 120)
        self.employee_table.setColumnWidth(5, 180)
        
        center_layout.addWidget(self.employee_table)
        
        center_widget.setLayout(center_layout)
        center_widget.setObjectName("centerPanel")
        return center_widget
    
    def apply_modern_styles(self):
        # Применяем централизованные стили
        self.setStyleSheet(get_main_stylesheet() + """
            #centerPanel {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
            
            QTableWidget::item:hover {
                background-color: #e3f2fd;
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
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                margin-left: 10px;
            }
        """)
    
    def load_data(self):
        cached_employees = self.cache.get_employees()
        if cached_employees is not None:
            self.current_employees = cached_employees
        else:
            self.current_employees = self.database.get_all_employees()
            self.cache.set_employees(self.current_employees)
        
        self.populate_table(self.current_employees)
        self.load_departments()
        self.load_positions()
        self.statistics_widget.update_statistics()
        self.statusBar().showMessage(f'Загружено сотрудников: {len(self.current_employees)}')
    
    def populate_table(self, employees):
        self.employee_table.setRowCount(0)
        
        for employee in employees:
            row = self.employee_table.rowCount()
            self.employee_table.insertRow(row)
            
            self.employee_table.setItem(row, 0, QTableWidgetItem(str(employee.id)))
            
            full_name = f"{employee.last_name} {employee.first_name}"
            if employee.middle_name:
                full_name += f" {employee.middle_name}"
            self.employee_table.setItem(row, 1, QTableWidgetItem(full_name))
            
            self.employee_table.setItem(row, 2, QTableWidgetItem(employee.position or '-'))
            
            department_name = '-'
            if employee.department_id:
                dept = self.database.get_department(employee.department_id)
                if dept:
                    department_name = dept.name
            self.employee_table.setItem(row, 3, QTableWidgetItem(department_name))
            
            phone = employee.work_phone or employee.mobile_phone or '-'
            self.employee_table.setItem(row, 4, QTableWidgetItem(phone))
            
            self.employee_table.setItem(row, 5, QTableWidgetItem(employee.email or '-'))
    
    def load_departments(self):
        self.department_tree.clear()
        departments = self.database.get_all_departments()
        
        all_item = QTreeWidgetItem(self.department_tree, ['Все сотрудники'])
        all_item.setData(0, Qt.ItemDataRole.UserRole, None)
        
        root_departments = [d for d in departments if d.parent_id is None]
        
        for dept in root_departments:
            self.add_department_to_tree(dept, all_item, departments)
        
        self.department_tree.expandAll()
    
    def add_department_to_tree(self, department, parent_item, all_departments):
        item = QTreeWidgetItem(parent_item, [department.name])
        item.setData(0, Qt.ItemDataRole.UserRole, department.id)
        
        child_departments = [d for d in all_departments if d.parent_id == department.id]
        for child in child_departments:
            self.add_department_to_tree(child, item, all_departments)
    
    def load_positions(self):
        self.position_filter.clear()
        self.position_filter.addItem('Все должности', None)
        
        positions = set()
        for emp in self.database.get_all_employees():
            if emp.position:
                positions.add(emp.position)
        
        for position in sorted(positions):
            self.position_filter.addItem(position, position)
    
    def filter_by_department(self, item):
        department_id = item.data(0, Qt.ItemDataRole.UserRole)
        
        if department_id is None:
            self.current_employees = self.database.get_all_employees()
        else:
            self.current_employees = self.database.filter_employees(department_id=department_id)
        
        self.populate_table(self.current_employees)
    
    def apply_filters(self):
        position = self.position_filter.currentData()
        
        if position:
            self.current_employees = self.database.filter_employees(position=position)
        else:
            self.current_employees = self.database.get_all_employees()
        
        self.populate_table(self.current_employees)
    
    def search_employees(self):
        query = self.search_input.text().strip()
        
        if not query:
            self.load_data()
            return
        
        if len(query) >= 3:
            self.settings_manager.add_search_to_history(query)
            self.update_search_completer()
        
        self.current_employees = self.database.search_employees(query)
        self.populate_table(self.current_employees)
        self.statusBar().showMessage(f'Найдено записей: {len(self.current_employees)}', 3000)
    
    def clear_search(self):
        self.search_input.clear()
        self.load_data()
    
    def update_search_completer(self):
        history = self.settings_manager.get_search_history()
        self.search_completer_model.setStringList(history)
    
    def advanced_search(self):
        dialog = AdvancedSearchDialog(self.database)
        if dialog.exec():
            criteria = dialog.get_search_criteria()
            
            if not criteria:
                QMessageBox.information(self, 'Поиск', 'Не указаны критерии поиска')
                return
            
            employees = self.database.get_all_employees()
            filtered_employees = []
            
            for emp in employees:
                match = True
                
                if 'fio' in criteria:
                    full_name = f"{emp.last_name} {emp.first_name} {emp.middle_name or ''}".lower()
                    if criteria['fio'].lower() not in full_name:
                        match = False
                
                if 'department_id' in criteria and emp.department_id != criteria['department_id']:
                    match = False
                
                if 'position' in criteria and emp.position:
                    if criteria['position'].lower() not in emp.position.lower():
                        match = False
                
                if 'email' in criteria and emp.email:
                    if criteria['email'].lower() not in emp.email.lower():
                        match = False
                
                if 'phone' in criteria:
                    phone_match = False
                    if emp.work_phone and criteria['phone'] in emp.work_phone:
                        phone_match = True
                    if emp.mobile_phone and criteria['phone'] in emp.mobile_phone:
                        phone_match = True
                    if not phone_match:
                        match = False
                
                if 'skills' in criteria and emp.skills:
                    if criteria['skills'].lower() not in emp.skills.lower():
                        match = False
                
                if 'hire_date_from' in criteria and emp.hire_date:
                    if str(emp.hire_date) < criteria['hire_date_from']:
                        match = False
                
                if 'hire_date_to' in criteria and emp.hire_date:
                    if str(emp.hire_date) > criteria['hire_date_to']:
                        match = False
                
                if 'has_photo' in criteria and not emp.photo:
                    match = False
                
                if match:
                    filtered_employees.append(emp)
            
            self.current_employees = filtered_employees
            self.populate_table(filtered_employees)
            self.statusBar().showMessage(f'Найдено: {len(filtered_employees)} сотрудников')
            
            if not filtered_employees:
                QMessageBox.information(self, 'Результаты поиска', 'Сотрудники по указанным критериям не найдены')
    
    def show_employee_card(self):
        selected_rows = self.employee_table.selectedItems()
        if not selected_rows:
            return
        
        row = self.employee_table.currentRow()
        employee_id = int(self.employee_table.item(row, 0).text())
        
        employee = self.database.get_employee(employee_id)
        if employee:
            while self.employee_card_layout.count():
                item = self.employee_card_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            card = EmployeeCard(employee, self.database)
            card.call_requested.connect(self.make_call)
            card.email_requested.connect(self.send_email)
            card.qr_requested.connect(self.generate_qr)
            
            # Анимация появления карточки
            card.setGraphicsEffect(QGraphicsOpacityEffect(card))
            card.graphicsEffect().setOpacity(0)
            
            self.employee_card_layout.addWidget(card)
            
            # Плавное появление
            fade_animation = QPropertyAnimation(card.graphicsEffect(), b"opacity")
            fade_animation.setDuration(400)
            fade_animation.setStartValue(0)
            fade_animation.setEndValue(1)
            fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            fade_animation.start()
    
    def add_employee(self):
        if not self.auth_manager.has_permission('add'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для добавления сотрудников!')
            return
        
        dialog = AddEditEmployeeDialog(self.database)
        if dialog.exec():
            self.cache.invalidate_employees()
            self.load_data()
            QMessageBox.information(self, 'Успех', 'Сотрудник успешно добавлен!')
    
    def edit_employee(self):
        if not self.auth_manager.has_permission('edit'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для редактирования!')
            return
        
        selected_rows = self.employee_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудника для редактирования!')
            return
        
        row = self.employee_table.currentRow()
        employee_id = int(self.employee_table.item(row, 0).text())
        
        employee = self.database.get_employee(employee_id)
        if employee:
            dialog = AddEditEmployeeDialog(self.database, employee)
            if dialog.exec():
                self.cache.invalidate_employees()
                self.load_data()
                QMessageBox.information(self, 'Успех', 'Данные сотрудника обновлены!')
    
    def delete_employee(self):
        if not self.auth_manager.has_permission('edit'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для удаления!')
            return
        
        selected_rows = self.employee_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудника для удаления!')
            return
        
        reply = QMessageBox.question(
            self, 
            'Подтверждение', 
            'Вы уверены, что хотите удалить выбранного сотрудника?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            row = self.employee_table.currentRow()
            employee_id = int(self.employee_table.item(row, 0).text())
            
            self.database.delete_employee(employee_id)
            self.cache.invalidate_employees()
            self.load_data()
            QMessageBox.information(self, 'Успех', 'Сотрудник удален!')
    
    def add_department(self):
        if not self.auth_manager.has_permission('add'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для добавления отделов!')
            return
        
        dialog = AddDepartmentDialog(self.database)
        if dialog.exec():
            self.load_departments()
            QMessageBox.information(self, 'Успех', 'Отдел успешно добавлен!')
    
    def import_csv(self):
        if not self.auth_manager.has_permission('add'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для импорта данных!')
            return
        
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            'Выберите CSV файл', 
            '', 
            'CSV файлы (*.csv)'
        )
        
        if filename:
            try:
                count = self.export_import.import_from_csv(filename)
                self.cache.invalidate_employees()
                self.load_data()
                QMessageBox.information(self, 'Успех', f'Импортировано записей: {count}')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось импортировать данные: {str(e)}')
    
    def import_excel(self):
        if not self.auth_manager.has_permission('add'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для импорта данных!')
            return
        
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            'Выберите Excel файл', 
            '', 
            'Excel файлы (*.xlsx *.xls)'
        )
        
        if filename:
            try:
                count = self.export_import.import_from_excel(filename)
                self.cache.invalidate_employees()
                self.load_data()
                QMessageBox.information(self, 'Успех', f'Импортировано записей: {count}')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось импортировать данные: {str(e)}')
    
    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            'Сохранить CSV файл', 
            '', 
            'CSV файлы (*.csv)'
        )
        
        if filename:
            try:
                self.export_import.export_to_csv(filename, self.current_employees)
                QMessageBox.information(self, 'Успех', 'Данные успешно экспортированы!')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {str(e)}')
    
    def export_excel(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            'Сохранить Excel файл', 
            '', 
            'Excel файлы (*.xlsx)'
        )
        
        if filename:
            try:
                self.export_import.export_to_excel(filename, self.current_employees)
                QMessageBox.information(self, 'Успех', 'Данные успешно экспортированы!')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {str(e)}')
    
    def export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            'Сохранить PDF файл', 
            '', 
            'PDF файлы (*.pdf)'
        )
        
        if filename:
            try:
                self.export_import.export_to_pdf(filename, self.current_employees)
                QMessageBox.information(self, 'Успех', 'Данные успешно экспортированы!')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {str(e)}')
    
    def export_business_card(self):
        selected_rows = self.employee_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудника для экспорта визитки!')
            return
        
        row = self.employee_table.currentRow()
        employee_id = int(self.employee_table.item(row, 0).text())
        employee = self.database.get_employee(employee_id)
        
        if employee:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                'Сохранить визитку',
                f'card_{employee.last_name}_{employee.first_name}.png',
                'PNG файлы (*.png)'
            )
            
            if filename:
                try:
                    card_data = self.card_generator.generate_business_card(employee, include_qr=True)
                    with open(filename, 'wb') as f:
                        f.write(card_data)
                    QMessageBox.information(self, 'Успех', 'Визитка успешно сохранена!')
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось создать визитку: {str(e)}')
    
    def export_contact_sheet(self):
        if not self.current_employees:
            QMessageBox.warning(self, 'Ошибка', 'Нет сотрудников для экспорта!')
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Сохранить лист контактов',
            'contacts_sheet.png',
            'PNG файлы (*.png)'
        )
        
        if filename:
            try:
                sheet_data = self.card_generator.generate_contact_sheet(
                    self.current_employees[:30],
                    'Список сотрудников'
                )
                with open(filename, 'wb') as f:
                    f.write(sheet_data)
                QMessageBox.information(self, 'Успех', f'Лист контактов успешно сохранен!\nЭкспортировано: {min(len(self.current_employees), 30)} сотрудников')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось создать лист контактов: {str(e)}')
    
    def make_call(self, phone_number):
        QMessageBox.information(
            self, 
            'Звонок', 
            f'Инициирован звонок на номер: {phone_number}\n\nДля интеграции с телефонией требуется настройка.'
        )
    
    def send_email(self, email):
        try:
            webbrowser.open(f'mailto:{email}')
        except Exception:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось открыть почтовый клиент!')
    
    def generate_qr(self, employee):
        try:
            qr_data = self.qr_generator.generate_qr_code(employee)
            
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                'Сохранить QR-код', 
                f'qr_{employee.last_name}_{employee.first_name}.png', 
                'PNG файлы (*.png)'
            )
            
            if filename:
                with open(filename, 'wb') as f:
                    f.write(qr_data)
                
                QMessageBox.information(self, 'Успех', 'QR-код успешно сохранен!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось создать QR-код: {str(e)}')
    
    def show_context_menu(self, position):
        menu = QMenu()
        
        edit_action = menu.addAction("Редактировать")
        delete_action = menu.addAction("Удалить")
        menu.addSeparator()
        export_vcard_action = menu.addAction("Экспортировать в vCard")
        
        action = menu.exec(self.employee_table.mapToGlobal(position))
        
        if action == edit_action:
            self.edit_employee()
        elif action == delete_action:
            self.delete_employee()
        elif action == export_vcard_action:
            self.export_vcard()
    
    def export_vcard(self):
        selected_rows = self.employee_table.selectedItems()
        if not selected_rows:
            return
        
        row = self.employee_table.currentRow()
        employee_id = int(self.employee_table.item(row, 0).text())
        
        employee = self.database.get_employee(employee_id)
        if employee:
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                'Сохранить vCard', 
                f'{employee.last_name}_{employee.first_name}.vcf', 
                'vCard файлы (*.vcf)'
            )
            
            if filename:
                try:
                    self.export_import.export_to_vcard(filename, employee)
                    QMessageBox.information(self, 'Успех', 'vCard успешно создан!')
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось создать vCard: {str(e)}')
    
    def check_birthdays(self):
        current_month = datetime.now().month
        birthday_employees = self.database.get_employees_by_birthday_month(current_month)
        
        if birthday_employees:
            message = f"В этом месяце дни рождения у {len(birthday_employees)} сотрудников:\n\n"
            for emp in birthday_employees[:5]:
                full_name = f"{emp.last_name} {emp.first_name}"
                message += f"• {full_name} - {emp.birth_date}\n"
            
            if len(birthday_employees) > 5:
                message += f"\n... и еще {len(birthday_employees) - 5}"
            
            QMessageBox.information(self, 'Напоминание о днях рождения', message)
    
    def export_json(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Сохранить JSON файл',
            '',
            'JSON файлы (*.json)'
        )
        
        if filename:
            try:
                self.json_exporter.export_employees(self.current_employees, filename)
                QMessageBox.information(self, 'Успех', f'Экспортировано записей: {len(self.current_employees)}')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {str(e)}')
    
    def duplicate_employee(self):
        if not self.auth_manager.has_permission('add'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для добавления сотрудников!')
            return
        
        selected_row = self.employee_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудника для дублирования!')
            return
        
        employee_id = int(self.employee_table.item(selected_row, 0).text())
        original_employee = self.database.get_employee(employee_id)
        
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            f'Дублировать сотрудника {original_employee.last_name} {original_employee.first_name}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            new_employee = Employee(
                id=None,
                last_name=original_employee.last_name + ' (копия)',
                first_name=original_employee.first_name,
                middle_name=original_employee.middle_name,
                department_id=original_employee.department_id,
                position=original_employee.position,
                work_phone=original_employee.work_phone,
                mobile_phone=original_employee.mobile_phone,
                email=original_employee.email,
                birth_date=original_employee.birth_date,
                hire_date=original_employee.hire_date,
                photo=original_employee.photo,
                room=original_employee.room,
                skills=original_employee.skills,
                manager_id=original_employee.manager_id,
                work_schedule=original_employee.work_schedule,
                telegram=original_employee.telegram,
                whatsapp=original_employee.whatsapp,
                skype=original_employee.skype
            )
            
            self.database.add_employee(new_employee)
            self.cache.invalidate_employees()
            self.load_data()
            QMessageBox.information(self, 'Успех', 'Сотрудник успешно дублирован!')
    
    def delete_multiple_employees(self):
        if not self.auth_manager.has_permission('delete'):
            QMessageBox.warning(self, 'Ошибка', 'У вас нет прав для удаления сотрудников!')
            return
        
        selected_items = self.employee_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудников для удаления!')
            return
        
        selected_rows = set(item.row() for item in selected_items)
        
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            f'Удалить {len(selected_rows)} сотрудников?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for row in sorted(selected_rows, reverse=True):
                employee_id = int(self.employee_table.item(row, 0).text())
                self.database.delete_employee(employee_id)
            
            self.cache.invalidate_employees()
            self.load_data()
            QMessageBox.information(self, 'Успех', f'Удалено сотрудников: {len(selected_rows)}')
    
    def show_context_menu(self, position):
        menu = QMenu()
        
        edit_action = menu.addAction('✏️ Редактировать')
        edit_action.triggered.connect(self.edit_employee)
        
        duplicate_action = menu.addAction('📋 Дублировать')
        duplicate_action.triggered.connect(self.duplicate_employee)
        
        menu.addSeparator()
        
        export_vcard_action = menu.addAction('💾 Экспорт vCard')
        export_vcard_action.triggered.connect(self.export_selected_vcard)
        
        export_png_action = menu.addAction('🖼️ Экспорт визитка PNG')
        export_png_action.triggered.connect(self.export_business_card)
        
        menu.addSeparator()
        
        delete_action = menu.addAction('🗑️ Удалить')
        delete_action.triggered.connect(self.delete_employee)
        
        menu.exec(self.employee_table.viewport().mapToGlobal(position))
    
    def on_table_double_click(self):
        self.edit_employee()
    
    def refresh_data(self):
        self.cache.invalidate_all()
        self.load_data()
        self.statusBar().showMessage('Данные обновлены', 3000)
    
    def focus_search(self):
        self.search_input.setFocus()
        self.search_input.selectAll()
    
    def show_settings(self):
        dialog = SettingsDialog(self.settings_manager, self)
        dialog.exec()
    
    def show_backup_dialog(self):
        dialog = BackupDialog(self.backup_manager, self)
        dialog.exec()
    
    def quick_backup(self):
        try:
            backup_path = self.backup_manager.create_backup(f'Ручное создание {datetime.now().strftime("%Y-%m-%d %H:%M")}')
            self.statusBar().showMessage(f'Резервная копия создана: {backup_path}', 5000)
            QMessageBox.information(self, 'Успех', f'Резервная копия создана:\n{backup_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось создать резервную копию:\n{str(e)}')
    
    def export_selected_vcard(self):
        selected_row = self.employee_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудника!')
            return
        
        employee_id = int(self.employee_table.item(selected_row, 0).text())
        employee = self.database.get_employee(employee_id)
        
        if employee:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                'Сохранить vCard',
                f'{employee.last_name}_{employee.first_name}.vcf',
                'vCard файлы (*.vcf)'
            )
            
            if filename:
                try:
                    self.export_import.export_to_vcard(filename, employee)
                    QMessageBox.information(self, 'Успех', 'vCard успешно создан!')
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось создать vCard: {str(e)}')
    
    def export_current_selection(self):
        if not self.current_employees:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для экспорта!')
            return
        
        from PyQt6.QtWidgets import QInputDialog
        
        formats = ['CSV', 'Excel', 'JSON']
        format_choice, ok = QInputDialog.getItem(
            self,
            'Выбор формата',
            f'Выберите формат для экспорта ({len(self.current_employees)} записей):',
            formats,
            0,
            False
        )
        
        if not ok:
            return
        
        if format_choice == 'CSV':
            filename, _ = QFileDialog.getSaveFileName(
                self,
                'Сохранить CSV файл',
                f'выборка_{len(self.current_employees)}_записей.csv',
                'CSV файлы (*.csv)'
            )
            if filename:
                try:
                    self.export_import.export_to_csv(filename, self.current_employees)
                    QMessageBox.information(self, 'Успех', f'Экспортировано записей: {len(self.current_employees)}')
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать: {str(e)}')
        
        elif format_choice == 'Excel':
            filename, _ = QFileDialog.getSaveFileName(
                self,
                'Сохранить Excel файл',
                f'выборка_{len(self.current_employees)}_записей.xlsx',
                'Excel файлы (*.xlsx)'
            )
            if filename:
                try:
                    self.export_import.export_to_excel(filename, self.current_employees)
                    QMessageBox.information(self, 'Успех', f'Экспортировано записей: {len(self.current_employees)}')
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать: {str(e)}')
        
        elif format_choice == 'JSON':
            filename, _ = QFileDialog.getSaveFileName(
                self,
                'Сохранить JSON файл',
                f'выборка_{len(self.current_employees)}_записей.json',
                'JSON файлы (*.json)'
            )
            if filename:
                try:
                    self.json_exporter.export_employees(self.current_employees, filename)
                    QMessageBox.information(self, 'Успех', f'Экспортировано записей: {len(self.current_employees)}')
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать: {str(e)}')
    
    def show_export_menu(self):
        """Показать меню экспорта"""
        from PyQt6.QtWidgets import QMenu
        
        menu = QMenu(self)
        
        csv_action = menu.addAction('📄 Экспорт в CSV')
        csv_action.triggered.connect(self.export_csv)
        
        excel_action = menu.addAction('📊 Экспорт в Excel')
        excel_action.triggered.connect(self.export_excel)
        
        pdf_action = menu.addAction('📑 Экспорт в PDF')
        pdf_action.triggered.connect(self.export_pdf)
        
        menu.addSeparator()
        
        json_action = menu.addAction('📦 Экспорт в JSON')
        json_action.triggered.connect(self.export_json)
        
        menu.addSeparator()
        
        current_action = menu.addAction('📋 Экспорт текущей выборки')
        current_action.triggered.connect(self.export_current_selection)
        
        # Показать меню в центре экрана
        menu.exec(self.mapToGlobal(self.rect().center()))
    
    def show_shortcuts(self):
        shortcuts_text = """
<h3>Горячие клавиши</h3>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>Клавиша</th><th>Действие</th></tr>
<tr><td><b>Ctrl+N</b></td><td>Добавить сотрудника</td></tr>
<tr><td><b>Ctrl+E</b></td><td>Редактировать сотрудника</td></tr>
<tr><td><b>Del</b></td><td>Удалить сотрудника</td></tr>
<tr><td><b>Ctrl+F</b></td><td>Поиск (фокус на поле)</td></tr>
<tr><td><b>Ctrl+Shift+F</b></td><td>Расширенный поиск</td></tr>
<tr><td><b>F5</b></td><td>Обновить данные</td></tr>
<tr><td><b>Ctrl+B</b></td><td>Создать резервную копию</td></tr>
<tr><td><b>Ctrl+,</b></td><td>Настройки</td></tr>
<tr><td><b>F1</b></td><td>Справка (горячие клавиши)</td></tr>
<tr><td><b>Двойной клик</b></td><td>Редактировать запись</td></tr>
<tr><td><b>Правый клик</b></td><td>Контекстное меню</td></tr>
</table>
<p><b>Подсказка:</b> История поиска сохраняется автоматически (последние 10 запросов)</p>
"""
        QMessageBox.information(self, 'Горячие клавиши', shortcuts_text)
    
    def show_about(self):
        QMessageBox.about(
            self,
            'О программе',
            '<h3>Каталог контактов сотрудников</h3>'
            '<p>Приложение для управления контактной информацией сотрудников организации.</p>'
            '<p><b>Возможности:</b> Горячие клавиши, Контекстное меню, Настройки, Резервное копирование, История поиска</p>'
            '<p><b>Технологии:</b> Python, PyQt6, SQLite</p>'
            '<p><b>Функции:</b></p>'
            '<ul>'
            '<li>Управление контактами сотрудников</li>'
            '<li>Поиск и фильтрация</li>'
            '<li>Организационная структура</li>'
            '<li>Импорт/экспорт данных</li>'
            '<li>Генерация QR-кодов</li>'
            '<li>Разграничение прав доступа</li>'
            '</ul>'
        )


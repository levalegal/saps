from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QPushButton, QSpinBox, QCheckBox, QLabel, QGroupBox,
                             QTabWidget, QWidget, QMessageBox)
from PyQt6.QtCore import Qt
from utils.settings_manager import SettingsManager

class SettingsDialog(QDialog):
    def __init__(self, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle('Настройки')
        self.setMinimumWidth(500)
        self.init_ui()
        self.load_current_settings()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        
        tabs.addTab(self.create_general_tab(), 'Общие')
        tabs.addTab(self.create_performance_tab(), 'Производительность')
        tabs.addTab(self.create_backup_tab(), 'Резервное копирование')
        
        layout.addWidget(tabs)
        
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton('Сбросить по умолчанию')
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton('Сохранить')
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('Отмена')
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def create_general_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        ui_group = QGroupBox('Интерфейс')
        ui_layout = QFormLayout()
        
        self.tooltips_check = QCheckBox()
        ui_layout.addRow('Показывать подсказки:', self.tooltips_check)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 16)
        self.font_size_spin.setSuffix(' pt')
        ui_layout.addRow('Размер шрифта таблицы:', self.font_size_spin)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        search_group = QGroupBox('Поиск')
        search_layout = QFormLayout()
        
        self.search_history_spin = QSpinBox()
        self.search_history_spin.setRange(5, 50)
        search_layout.addRow('Размер истории поиска:', self.search_history_spin)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_performance_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        cache_group = QGroupBox('Кэширование')
        cache_layout = QFormLayout()
        
        self.cache_ttl_spin = QSpinBox()
        self.cache_ttl_spin.setRange(60, 3600)
        self.cache_ttl_spin.setSuffix(' сек')
        cache_layout.addRow('Время жизни кэша (TTL):', self.cache_ttl_spin)
        
        info_label = QLabel('Рекомендуется: 300 секунд (5 минут)')
        info_label.setStyleSheet('color: gray; font-size: 9pt;')
        cache_layout.addRow('', info_label)
        
        cache_group.setLayout(cache_layout)
        layout.addWidget(cache_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_backup_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        backup_group = QGroupBox('Автоматическое резервное копирование')
        backup_layout = QFormLayout()
        
        self.auto_backup_check = QCheckBox()
        backup_layout.addRow('Включить автобэкап:', self.auto_backup_check)
        
        self.backup_interval_spin = QSpinBox()
        self.backup_interval_spin.setRange(1, 168)
        self.backup_interval_spin.setSuffix(' ч')
        backup_layout.addRow('Интервал создания:', self.backup_interval_spin)
        
        self.max_backups_spin = QSpinBox()
        self.max_backups_spin.setRange(3, 100)
        backup_layout.addRow('Максимум резервных копий:', self.max_backups_spin)
        
        info_label = QLabel('Старые копии удаляются автоматически')
        info_label.setStyleSheet('color: gray; font-size: 9pt;')
        backup_layout.addRow('', info_label)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def load_current_settings(self):
        self.tooltips_check.setChecked(
            self.settings_manager.get('show_tooltips', True)
        )
        self.font_size_spin.setValue(
            self.settings_manager.get('table_font_size', 10)
        )
        self.search_history_spin.setValue(
            self.settings_manager.get('search_history_size', 10)
        )
        self.cache_ttl_spin.setValue(
            self.settings_manager.get('cache_ttl', 300)
        )
        self.auto_backup_check.setChecked(
            self.settings_manager.get('auto_backup', True)
        )
        self.backup_interval_spin.setValue(
            self.settings_manager.get('backup_interval', 24)
        )
        self.max_backups_spin.setValue(
            self.settings_manager.get('max_backups', 10)
        )
    
    def save_settings(self):
        self.settings_manager.set('show_tooltips', self.tooltips_check.isChecked())
        self.settings_manager.set('table_font_size', self.font_size_spin.value())
        self.settings_manager.set('search_history_size', self.search_history_spin.value())
        self.settings_manager.set('cache_ttl', self.cache_ttl_spin.value())
        self.settings_manager.set('auto_backup', self.auto_backup_check.isChecked())
        self.settings_manager.set('backup_interval', self.backup_interval_spin.value())
        self.settings_manager.set('max_backups', self.max_backups_spin.value())
        
        QMessageBox.information(
            self,
            'Настройки сохранены',
            'Некоторые изменения вступят в силу после перезапуска приложения.'
        )
        self.accept()
    
    def reset_to_defaults(self):
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            'Сбросить все настройки к значениям по умолчанию?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.settings_manager.reset_to_defaults()
            self.load_current_settings()
            QMessageBox.information(self, 'Готово', 'Настройки сброшены!')





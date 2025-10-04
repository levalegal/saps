from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGroupBox, QFrame, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from database.database import Database
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class StatisticsChart(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#f5f6fa')
        super().__init__(self.fig)
        self.setParent(parent)

class ModernStatisticsWidget(QWidget):
    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border-radius: 5px;
                margin-left: 10px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 10pt;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 10pt;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #229954, stop:1 #1e8449);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel('📊 Статистика и аналитика')
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
        
        summary_group = QGroupBox('📈 Общая информация')
        summary_layout = QVBoxLayout()
        
        self.total_employees_label = QLabel('Всего сотрудников: 0')
        self.total_employees_label.setStyleSheet("font-size: 11pt; font-weight: bold; padding: 5px;")
        summary_layout.addWidget(self.total_employees_label)
        
        self.avg_age_label = QLabel('Средний возраст: -')
        self.avg_age_label.setStyleSheet("padding: 5px;")
        summary_layout.addWidget(self.avg_age_label)
        
        self.with_photo_label = QLabel('С фото: 0 (0%)')
        self.with_photo_label.setStyleSheet("padding: 5px;")
        summary_layout.addWidget(self.with_photo_label)
        
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        self.dept_chart_canvas = StatisticsChart(self, width=5, height=3, dpi=80)
        layout.addWidget(self.dept_chart_canvas)
        
        self.position_chart_canvas = StatisticsChart(self, width=5, height=3, dpi=80)
        layout.addWidget(self.position_chart_canvas)
        
        refresh_button = QPushButton('🔄 Обновить статистику')
        refresh_button.clicked.connect(self.update_statistics)
        layout.addWidget(refresh_button)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.update_statistics()
    
    def update_statistics(self):
        employees = self.database.get_all_employees()
        departments = self.database.get_all_departments()
        
        total_count = len(employees)
        self.total_employees_label.setText(f'👥 Всего сотрудников: {total_count}')
        
        if total_count > 0:
            with_photo = sum(1 for emp in employees if emp.photo)
            photo_percent = (with_photo / total_count) * 100
            self.with_photo_label.setText(f'📷 С фото: {with_photo} ({photo_percent:.1f}%)')
            
            ages = []
            from datetime import datetime
            for emp in employees:
                if emp.birth_date:
                    birth_date = datetime.strptime(str(emp.birth_date), '%Y-%m-%d')
                    age = (datetime.now() - birth_date).days // 365
                    ages.append(age)
            
            if ages:
                avg_age = sum(ages) / len(ages)
                self.avg_age_label.setText(f'🎂 Средний возраст: {avg_age:.1f} лет')
            else:
                self.avg_age_label.setText('🎂 Средний возраст: -')
        else:
            self.with_photo_label.setText('📷 С фото: 0 (0%)')
            self.avg_age_label.setText('🎂 Средний возраст: -')
        
        self.draw_department_chart(employees, departments)
        self.draw_position_chart(employees)
    
    def draw_department_chart(self, employees, departments):
        self.dept_chart_canvas.fig.clear()
        ax = self.dept_chart_canvas.fig.add_subplot(111)
        
        dept_counts = {}
        for dept in departments:
            count = sum(1 for emp in employees if emp.department_id == dept.id)
            if count > 0:
                dept_counts[dept.name] = count
        
        no_dept = sum(1 for emp in employees if emp.department_id is None)
        if no_dept > 0:
            dept_counts['Без отдела'] = no_dept
        
        if dept_counts:
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', 
                      '#1abc9c', '#34495e', '#e67e22', '#95a5a6']
            
            wedges, texts, autotexts = ax.pie(
                dept_counts.values(), 
                labels=dept_counts.keys(),
                autopct='%1.1f%%',
                colors=colors[:len(dept_counts)],
                startangle=90,
                textprops={'fontsize': 9, 'weight': 'bold'}
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_weight('bold')
            
            ax.set_title('Распределение по отделам', fontsize=12, fontweight='bold', pad=20)
        else:
            ax.text(0.5, 0.5, 'Нет данных', ha='center', va='center', 
                   fontsize=14, color='#95a5a6')
        
        ax.axis('equal')
        self.dept_chart_canvas.draw()
    
    def draw_position_chart(self, employees):
        self.position_chart_canvas.fig.clear()
        ax = self.position_chart_canvas.fig.add_subplot(111)
        
        position_counts = {}
        for emp in employees:
            pos = emp.position if emp.position else 'Не указана'
            position_counts[pos] = position_counts.get(pos, 0) + 1
        
        if position_counts:
            sorted_positions = sorted(position_counts.items(), key=lambda x: x[1], reverse=True)
            top_positions = sorted_positions[:8]
            
            positions = [p[0][:20] + '...' if len(p[0]) > 20 else p[0] for p in top_positions]
            counts = [p[1] for p in top_positions]
            
            colors = ['#3498db' if i == 0 else '#5dade2' for i in range(len(positions))]
            
            bars = ax.barh(positions, counts, color=colors)
            
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f' {int(width)}',
                       ha='left', va='center', fontweight='bold', fontsize=9)
            
            ax.set_xlabel('Количество сотрудников', fontsize=10, fontweight='bold')
            ax.set_title('Топ должностей', fontsize=12, fontweight='bold', pad=15)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            plt.setp(ax.get_yticklabels(), fontsize=9)
            plt.setp(ax.get_xticklabels(), fontsize=9)
        else:
            ax.text(0.5, 0.5, 'Нет данных', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14, color='#95a5a6')
        
        self.position_chart_canvas.fig.tight_layout()
        self.position_chart_canvas.draw()




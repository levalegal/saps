"""
Централизованные стили для всего приложения
Премиум дизайн с единым стилем и плавными эффектами
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

# ============================================================================
# ЦВЕТОВАЯ ПАЛИТРА - Единая система
# ============================================================================

class ColorPalette:
    """Централизованная палитра цветов"""
    
    # Синие (основные)
    PRIMARY = "#2196F3"
    PRIMARY_DARK = "#1976D2"
    PRIMARY_LIGHT = "#64B5F6"
    PRIMARY_LIGHTER = "#90CAF9"
    PRIMARY_LIGHTEST = "#BBDEFB"
    PRIMARY_DARKER = "#1565C0"
    PRIMARY_DARKEST = "#0D47A1"
    
    # Серые (фоны)
    BACKGROUND_LIGHT = "#FFFFFF"
    BACKGROUND_GRAY = "#F5F7FA"
    BACKGROUND_DARK = "#E9ECEF"
    SURFACE = "#FFFFFF"
    SURFACE_HOVER = "#F8F9FA"
    
    # Границы
    BORDER_LIGHT = "#E0E0E0"
    BORDER_MEDIUM = "#C0C0C0"
    BORDER_DARK = "#9E9E9E"
    
    # Текст
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#6C757D"
    TEXT_DISABLED = "#ADB5BD"
    TEXT_INVERSE = "#FFFFFF"
    
    # Статусы
    SUCCESS = "#28A745"
    WARNING = "#FFC107"
    ERROR = "#DC3545"
    INFO = "#17A2B8"


def get_main_stylesheet():
    """Главный стиль для всего приложения с плавными анимациями"""
    return f"""
        /* ============================================ */
        /* ГЛАВНОЕ ОКНО - Градиентный фон */
        /* ============================================ */
        
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #F5F7FA, 
                stop:0.4 #F0F2F5, 
                stop:1 #E9ECEF);
        }}
        
        /* ============================================ */
        /* TOOLBAR - С эффектами */
        /* ============================================ */
        
        QToolBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFFFFF, stop:1 #F8F9FA);
            border: none;
            border-bottom: 3px solid {ColorPalette.PRIMARY};
            padding: 12px;
            spacing: 10px;
        }}
        
        QToolBar QToolButton {{
            background-color: transparent;
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 12px 18px;
            font-size: 11pt;
            font-weight: 600;
            color: #212529;
        }}
        
        QToolBar QToolButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #E3F2FD, stop:1 #BBDEFB);
            border: 2px solid #90CAF9;
        }}
        
        QToolBar QToolButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #90CAF9, stop:1 #64B5F6);
        }}
        
        /* ============================================ */
        /* MENU BAR - Градиент с эффектами */
        /* ============================================ */
        
        QMenuBar {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ColorPalette.PRIMARY_DARK}, 
                stop:0.3 {ColorPalette.PRIMARY}, 
                stop:0.7 {ColorPalette.PRIMARY}, 
                stop:1 {ColorPalette.PRIMARY_DARK});
            color: white;
            padding: 8px;
            font-size: 10pt;
            font-weight: 600;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 12px 20px;
            border-radius: 8px;
            margin: 0 2px;
        }}
        
        QMenuBar::item:selected {{
            background-color: rgba(255, 255, 255, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        QMenuBar::item:pressed {{
            background-color: rgba(255, 255, 255, 0.35);
        }}
        
        QMenu {{
            background-color: white;
            border: 2px solid {ColorPalette.PRIMARY};
            border-radius: 12px;
            padding: 10px;
        }}
        
        QMenu::item {{
            padding: 12px 35px 12px 20px;
            border-radius: 8px;
            margin: 3px;
            font-size: 10pt;
        }}
        
        QMenu::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ColorPalette.PRIMARY}, stop:1 {ColorPalette.PRIMARY_DARK});
            color: white;
        }}
        
        QMenu::separator {{
            height: 2px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 transparent, 
                stop:0.5 {ColorPalette.BORDER_LIGHT}, 
                stop:1 transparent);
            margin: 6px 12px;
        }}
        
        /* ============================================ */
        /* STATUS BAR - С градиентом */
        /* ============================================ */
        
        QStatusBar {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #F8F9FA, stop:1 #E9ECEF);
            border-top: 3px solid {ColorPalette.PRIMARY};
            color: #212529;
            font-size: 10pt;
            font-weight: 500;
            padding: 10px;
        }}
        
        /* ============================================ */
        /* BUTTONS - С плавными градиентами */
        /* ============================================ */
        
        QPushButton {{
            border: none;
            border-radius: 12px;
            padding: 14px 28px;
            font-size: 11pt;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        
        QPushButton:default {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ColorPalette.PRIMARY}, 
                stop:0.5 {ColorPalette.PRIMARY_DARK}, 
                stop:1 {ColorPalette.PRIMARY});
            color: white;
        }}
        
        QPushButton:default:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ColorPalette.PRIMARY_DARK}, 
                stop:0.5 {ColorPalette.PRIMARY_DARKER}, 
                stop:1 {ColorPalette.PRIMARY_DARKEST});
            border: 2px solid #BBDEFB;
        }}
        
        QPushButton:default:pressed {{
            background: {ColorPalette.PRIMARY_DARKEST};
            padding: 15px 26px 13px 30px;
        }}
        
        QPushButton:!default {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #757575, stop:1 #616161);
            color: white;
        }}
        
        QPushButton:!default:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #616161, stop:1 #424242);
        }}
        
        QPushButton:!default:pressed {{
            background: #424242;
            padding: 15px 26px 13px 30px;
        }}
        
        /* ============================================ */
        /* LINE EDITS - С фокус-эффектами */
        /* ============================================ */
        
        QLineEdit, QTextEdit {{
            border: 2px solid {ColorPalette.BORDER_LIGHT};
            border-radius: 12px;
            padding: 14px 20px;
            font-size: 12pt;
            background-color: {ColorPalette.SURFACE};
            selection-background-color: {ColorPalette.PRIMARY};
            color: {ColorPalette.TEXT_PRIMARY};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border: 2px solid {ColorPalette.PRIMARY};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFFFFF, stop:1 #F8F9FA);
        }}
        
        QLineEdit:hover, QTextEdit:hover {{
            border: 2px solid {ColorPalette.PRIMARY_LIGHTER};
            background-color: {ColorPalette.SURFACE_HOVER};
        }}
        
        /* ============================================ */
        /* TABLES - С красивыми заголовками */
        /* ============================================ */
        
                 QTableWidget {{
             background-color: white;
             border: 2px solid {ColorPalette.BORDER_LIGHT};
             border-radius: 12px;
             gridline-color: {ColorPalette.BORDER_LIGHT};
             selection-background-color: {ColorPalette.PRIMARY_LIGHTEST};
             selection-color: {ColorPalette.PRIMARY_DARK};
             font-size: 10pt;
             alternate-background-color: #F8F9FA;
         }}
         
         QTableWidget::item {{
             padding: 12px;
             border: none;
         }}
         
         QTableWidget::item:selected {{
             background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {ColorPalette.PRIMARY_LIGHTEST}, 
                 stop:1 {ColorPalette.PRIMARY_LIGHT});
             color: {ColorPalette.PRIMARY_DARK};
             font-weight: 600;
         }}
         
         QTableWidget::item:hover {{
             background-color: #E3F2FD;
         }}
         
         QTableWidget::item:selected:hover {{
             background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 #BBDEFB, 
                 stop:1 #90CAF9);
         }}
        
        QHeaderView::section {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ColorPalette.PRIMARY_LIGHT}, 
                stop:1 {ColorPalette.PRIMARY});
            color: white;
            padding: 12px;
            border: none;
            font-weight: 700;
            font-size: 10pt;
        }}
        
        /* ============================================ */
        /* TREE WIDGET - С hover эффектами */
        /* ============================================ */
        
        QTreeWidget {{
            background-color: white;
            border: 1px solid {ColorPalette.BORDER_LIGHT};
            border-radius: 12px;
            font-size: 10pt;
        }}
        
        QTreeWidget::item {{
            padding: 8px;
            border-radius: 8px;
        }}
        
        QTreeWidget::item:hover {{
            background-color: {ColorPalette.BACKGROUND_GRAY};
        }}
        
        QTreeWidget::item:selected {{
            background-color: {ColorPalette.PRIMARY_LIGHTEST};
            color: {ColorPalette.PRIMARY_DARK};
            font-weight: 600;
        }}
        
        /* ============================================ */
        /* COMBOBOX - С красивой стрелкой */
        /* ============================================ */
        
        QComboBox {{
            border: 2px solid {ColorPalette.BORDER_LIGHT};
            border-radius: 12px;
            padding: 10px 15px;
            font-size: 11pt;
            background-color: {ColorPalette.SURFACE};
            color: {ColorPalette.TEXT_PRIMARY};
        }}
        
        QComboBox:hover {{
            border: 2px solid {ColorPalette.PRIMARY_LIGHT};
        }}
        
        QComboBox:focus {{
            border: 2px solid {ColorPalette.PRIMARY};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFFFFF, stop:1 #F8F9FA);
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {ColorPalette.PRIMARY};
            margin-right: 10px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {ColorPalette.SURFACE};
            border: 2px solid {ColorPalette.PRIMARY};
            border-radius: 12px;
            selection-background-color: {ColorPalette.PRIMARY_LIGHTEST};
            padding: 5px;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 8px 15px;
            border-radius: 6px;
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background-color: {ColorPalette.PRIMARY_LIGHT};
            color: {ColorPalette.TEXT_INVERSE};
        }}
        
        /* ============================================ */
        /* SCROLLBARS - С эффектами */
        /* ============================================ */
        
        QScrollBar:vertical {{
            background: {ColorPalette.BACKGROUND_GRAY};
            width: 14px;
            border: none;
            border-radius: 7px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ColorPalette.PRIMARY_LIGHT}, 
                stop:1 {ColorPalette.PRIMARY});
            border-radius: 7px;
            min-height: 35px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ColorPalette.PRIMARY}, 
                stop:1 {ColorPalette.PRIMARY_DARK});
        }}
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        
        QScrollBar:horizontal {{
            background: {ColorPalette.BACKGROUND_GRAY};
            height: 14px;
            border: none;
            border-radius: 7px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ColorPalette.PRIMARY_LIGHT}, 
                stop:1 {ColorPalette.PRIMARY});
            border-radius: 7px;
            min-width: 35px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ColorPalette.PRIMARY}, 
                stop:1 {ColorPalette.PRIMARY_DARK});
        }}
        
        /* ============================================ */
        /* SPLITTER - Интерактивный */
        /* ============================================ */
        
        QSplitter::handle {{
            background-color: {ColorPalette.BORDER_LIGHT};
        }}
        
        QSplitter::handle:horizontal {{
            width: 4px;
        }}
        
        QSplitter::handle:vertical {{
            height: 4px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {ColorPalette.PRIMARY_LIGHTER};
        }}
        
        /* ============================================ */
        /* LABELS - С четким текстом */
        /* ============================================ */
        
        QLabel {{
            color: {ColorPalette.TEXT_PRIMARY};
            font-size: 10pt;
        }}
        
        /* ============================================ */
        /* FRAMES & PANELS */
        /* ============================================ */
        
                 QFrame {{
             background-color: {ColorPalette.SURFACE};
             border-radius: 12px;
         }}
         
         /* ============================================ */
         /* ДОПОЛНИТЕЛЬНЫЕ ЭФФЕКТЫ */
         /* ============================================ */
         
                   /* Общие эффекты переходов */
          QWidget {{
          }}
         
         /* Улучшенные тени и эффекты глубины */
         QTableWidget {{
             selection-background-color: {ColorPalette.PRIMARY_LIGHTEST};
         }}
         
                   /* Анимация для кнопок */
          QPushButton {{
          }}
         
         /* Эффект свечения для активных элементов */
         QPushButton:default:focus {{
             border: 2px solid #BBDEFB;
             outline: none;
         }}
         
         /* Анимированная полоса прокрутки */
         QScrollBar::handle:vertical:pressed {{
             background: {ColorPalette.PRIMARY_DARK};
         }}
         
         QScrollBar::handle:horizontal:pressed {{
             background: {ColorPalette.PRIMARY_DARK};
         }}
         
         /* Эффект для выбранного элемента дерева */
         QTreeWidget::item:selected:active {{
             background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {ColorPalette.PRIMARY_LIGHTEST}, 
                 stop:1 {ColorPalette.PRIMARY_LIGHT});
         }}
         
         /* Эффект для активной вкладки (если есть) */
         QTabWidget::pane {{
             border: 1px solid {ColorPalette.BORDER_LIGHT};
             border-radius: 8px;
             background: {ColorPalette.SURFACE};
         }}
         
         QTabBar::tab {{
             background: {ColorPalette.BACKGROUND_GRAY};
             color: {ColorPalette.TEXT_SECONDARY};
             padding: 10px 20px;
             border-top-left-radius: 8px;
             border-top-right-radius: 8px;
             margin-right: 2px;
         }}
         
         QTabBar::tab:selected {{
             background: {ColorPalette.PRIMARY};
             color: white;
             font-weight: 600;
         }}
         
         QTabBar::tab:hover:!selected {{
             background: {ColorPalette.PRIMARY_LIGHTEST};
             color: {ColorPalette.PRIMARY_DARK};
         }}
         
         /* Группы и рамки */
         QGroupBox {{
             border: 2px solid {ColorPalette.BORDER_LIGHT};
             border-radius: 12px;
             margin-top: 12px;
             padding-top: 16px;
             font-weight: 600;
             font-size: 11pt;
         }}
         
         QGroupBox::title {{
             subcontrol-origin: margin;
             subcontrol-position: top left;
             padding: 6px 16px;
             background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {ColorPalette.PRIMARY}, stop:1 {ColorPalette.PRIMARY_DARK});
             color: white;
             border-radius: 8px;
             margin-left: 12px;
         }}
         
         /* Радио-кнопки и чекбоксы */
         QRadioButton {{
             spacing: 8px;
             color: {ColorPalette.TEXT_PRIMARY};
         }}
         
         QRadioButton::indicator {{
             width: 18px;
             height: 18px;
             border-radius: 9px;
             border: 2px solid {ColorPalette.PRIMARY};
         }}
         
         QRadioButton::indicator:checked {{
             background-color: {ColorPalette.PRIMARY};
             border: 2px solid {ColorPalette.PRIMARY};
         }}
         
         QCheckBox {{
             spacing: 8px;
             color: {ColorPalette.TEXT_PRIMARY};
         }}
         
         QCheckBox::indicator {{
             width: 18px;
             height: 18px;
             border: 2px solid {ColorPalette.PRIMARY};
             border-radius: 4px;
         }}
         
         QCheckBox::indicator:checked {{
             background-color: {ColorPalette.PRIMARY};
             border: 2px solid {ColorPalette.PRIMARY};
         }}
         
         /* Slider */
         QSlider::groove:horizontal {{
             border: 1px solid {ColorPalette.BORDER_LIGHT};
             height: 8px;
             background: {ColorPalette.BACKGROUND_GRAY};
             border-radius: 4px;
         }}
         
         QSlider::handle:horizontal {{
             background: {ColorPalette.PRIMARY};
             border: 2px solid white;
             width: 20px;
             height: 20px;
             border-radius: 10px;
             margin: -6px 0;
         }}
         
         QSlider::handle:horizontal:hover {{
             background: {ColorPalette.PRIMARY_DARK};
         }}
         
         /* Progress Bar */
         QProgressBar {{
             border: 2px solid {ColorPalette.BORDER_LIGHT};
             border-radius: 8px;
             text-align: center;
             font-weight: 600;
             color: white;
         }}
         
         QProgressBar::chunk {{
             background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {ColorPalette.PRIMARY}, 
                 stop:0.5 {ColorPalette.PRIMARY_DARK}, 
                 stop:1 {ColorPalette.PRIMARY});
             border-radius: 6px;
         }}
         
         /* Tool Tip */
         QToolTip {{
             background-color: {ColorPalette.PRIMARY_DARK};
             color: white;
             border: none;
             border-radius: 8px;
             padding: 8px 12px;
             font-size: 9pt;
         }}
         
         /* Spin Box */
         QSpinBox, QDoubleSpinBox {{
             border: 2px solid {ColorPalette.BORDER_LIGHT};
             border-radius: 8px;
             padding: 6px 10px;
             background-color: {ColorPalette.SURFACE};
         }}
         
         QSpinBox:focus, QDoubleSpinBox:focus {{
             border: 2px solid {ColorPalette.PRIMARY};
         }}
         
         QSpinBox::up-button, QSpinBox::down-button,
         QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
             background-color: {ColorPalette.PRIMARY};
             border: none;
             width: 20px;
         }}
         
                   QSpinBox::up-button:hover, QSpinBox::down-button:hover,
          QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
              background-color: {ColorPalette.PRIMARY_DARK};
          }}
          
          /* ============================================ */
          /* ДОПОЛНИТЕЛЬНЫЕ ПРЕМИУМ ЭФФЕКТЫ */
          /* ============================================ */
          
          /* Эффект тени для карточек */
          QGroupBox {{
              background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                  stop:0 {ColorPalette.SURFACE}, 
                  stop:1 {ColorPalette.SURFACE_HOVER});
          }}
          
                     /* Анимация пульсации для активных кнопок */
           QPushButton:default:focus {{
           }}
           
           /* Эффект свечения при наведении */
           QPushButton:hover {{
           }}
           
           /* Эффект увеличения при нажатии */
           QPushButton:pressed {{
           }}
          
                     /* Плавное изменение цвета таблицы */
           QTableWidget::item {{
           }}
          
          /* Улучшенный эффект hover для деревьев */
          QTreeWidget::item:hover {{
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop:0 {ColorPalette.BACKGROUND_GRAY}, 
                  stop:1 {ColorPalette.PRIMARY_LIGHTEST});
              padding-left: 5px;
          }}
          
                     /* Анимация для полей ввода */
           QLineEdit:focus {{
               border: 3px solid {ColorPalette.PRIMARY};
           }}
     """

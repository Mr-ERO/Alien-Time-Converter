import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QDialog, QDialogButtonBox
from PyQt6.QtCore import QSettings
from PyQt6.QtCore import QDate
from datetime import datetime, timedelta

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("设置")

        # 外星自转时间
        self.spinBox_rotation = QSpinBox()
        self.spinBox_rotation.setMinimum(1)
        self.spinBox_rotation.setMaximum(1000000)

        # 外星公转时间
        self.spinBox_orbital = QSpinBox()
        self.spinBox_orbital.setMinimum(1)
        self.spinBox_orbital.setMaximum(1000000)

        # 外星人一个月等于多少外星日
        self.spinBox_month_days = QSpinBox()
        self.spinBox_month_days.setMinimum(1)
        self.spinBox_month_days.setMaximum(1000)


        # 外星日历元年对应地球日期
        self.dateEdit_epoch = QDateEdit()
        self.dateEdit_epoch.setCalendarPopup(True)

        # 时间流速比例
        self.doubleSpinBox_time_ratio = QDoubleSpinBox()
        self.doubleSpinBox_time_ratio.setMinimum(0.01)
        self.doubleSpinBox_time_ratio.setMaximum(100.0)
        self.doubleSpinBox_time_ratio.setSingleStep(0.01)

        # 布局
        layout = QGridLayout(self)
        layout.addWidget(QLabel("外星自转时间（小时）:"), 0, 0)
        layout.addWidget(self.spinBox_rotation, 0, 1)
        layout.addWidget(QLabel("外星公转时间（天）:"), 1, 0)
        layout.addWidget(self.spinBox_orbital, 1, 1)
        layout.addWidget(QLabel("一个月的天数（天）:"), 2, 0)
        layout.addWidget(self.spinBox_month_days, 2, 1)
        layout.addWidget(QLabel("外星日历元年对应地球日期:"), 4, 0)
        layout.addWidget(self.dateEdit_epoch, 4, 1)
        layout.addWidget(QLabel("时间流速比例（外星/地球）:"), 5, 0)
        layout.addWidget(self.doubleSpinBox_time_ratio, 5, 1)

        # 添加按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 6, 0, 1, 2)
        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_settings)
        # 加载按钮
        self.load_button = QPushButton("加载", self)
        self.load_button.clicked.connect(self.load_settings)
        # 添加按钮到布局
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
    def get_settings(self):
        settings = {
            'rotation': self.spinBox_rotation.value(),
            'orbital': self.spinBox_orbital.value(),
            'month_days': self.spinBox_month_days.value(),
            'epoch': self.dateEdit_epoch.date().toPyDate(),
            'time_ratio': self.doubleSpinBox_time_ratio.value(),
        }
        return settings

    def load_settings(self):
        qsettings = QSettings('MyCompany', 'MyApp')
        # 使用 QSettings 加载设置
        settings = {
            'rotation': qsettings.value('rotation', type=int),
            'orbital': qsettings.value('orbital', type=int),
            'month_days': qsettings.value('month_days', type=int),
            'epoch': qsettings.value('epoch'),  # 读取为 QVariant 类型
            'time_ratio': qsettings.value('time_ratio', type=float),
        }
        # 设置控件的值
        self.spinBox_rotation.setValue(settings['rotation'])
        self.spinBox_orbital.setValue(settings['orbital'])
        self.spinBox_month_days.setValue(settings['month_days'])
        # 如果 'epoch' 为空，则设置当前日期为默认值
        if not settings['epoch']:
            default_date = QDate.currentDate()  # 获取当前日期
            self.dateEdit_epoch.setDate(default_date)
        else:
            # 尝试将 QVariant 转换为 QDate
            try:
                qdate = settings['epoch'].toDate()
                self.dateEdit_epoch.setDate(qdate)
            except AttributeError:
                # 如果失败，尝试将 QVariant 转换为 QString
                try:
                    qstring = settings['epoch'].toString()
                    self.dateEdit_epoch.setDate(QDate.fromString(qstring, "yyyy-MM-dd"))
                except Exception as e:
                    print(f"Error: Unable to load epoch value. {e}")
        self.doubleSpinBox_time_ratio.setValue(settings['time_ratio'])
        print("Settings loaded")
    def save_settings(self):
        settings = self.get_settings()
        qsettings = QSettings('MyCompany', 'MyApp')
        for key, value in settings.items():
            if key == 'epoch':
                # 将 QDate 对象转换为 "yyyy-MM-dd" 格式的字符串
                value = QDate.fromString(value.strftime("%Y-%m-%d"), "yyyy-MM-dd")
                value = value.toString("yyyy-MM-dd")
            qsettings.setValue(key, value)
        print("Settings saved")



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("外星时间换算器")

        # 设置按钮
        self.settings_button = QPushButton("设置", self)
        self.settings_button.clicked.connect(self.open_settings)

        # 地球日期输入
        self.line_edit_earth_date = QLineEdit(self)
        self.label_earth_date = QLabel("地球日期(yyyy-MM-dd):")
        # 外星日期输入
        self.line_edit_alien_date = QLineEdit(self)
        self.label_alien_date = QLabel("外星日期:")
        # 地球转外星按钮
        self.convert_earth_to_alien_button = QPushButton("地球转外星", self)
        self.convert_earth_to_alien_button.clicked.connect(self.convert_earth_to_alien)

        # 外星转地球按钮
        self.convert_alien_to_earth_button = QPushButton("外星转地球", self)
        self.convert_alien_to_earth_button.clicked.connect(self.convert_alien_to_earth)

        # 布局
        layout = QGridLayout()
        layout.addWidget(self.label_earth_date, 0, 0)
        layout.addWidget(self.line_edit_earth_date, 0, 1)
        layout.addWidget(self.convert_earth_to_alien_button, 0, 2)
        layout.addWidget(self.label_alien_date, 1, 0)
        layout.addWidget(self.line_edit_alien_date, 1, 1)
        layout.addWidget(self.convert_alien_to_earth_button, 1, 2)
        layout.addWidget(self.settings_button)


        # 创建中心窗口
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 初始化设置
        self.settings = None

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            dialog.save_settings()  # 保存设置
            self.settings = dialog.get_settings()
            print(self.settings)  # 这里可以替换为保存设置的代码
    def load_settings(self):
        dialog = SettingsDialog(self)
        dialog.load_settings()
        self.settings = dialog.get_settings()

    def convert_earth_to_alien(self):
        # 获取地球日期输入
        earth_date_str = self.line_edit_earth_date.text()
        earth_date = QDate.fromString(earth_date_str, "yyyy-MM-dd")
        # 获取用户设置
        settings = self.settings
        if not settings:
            print("Error: Settings not loaded.")
            return
        # 计算地球日期与元年的差值
        epoch_date_str = settings['epoch'].strftime("%Y-%m-%d")
        epoch_date = QDate.fromString(epoch_date_str, "yyyy-MM-dd")
        delta_days = epoch_date.daysTo(earth_date)
        print(delta_days)
        print(epoch_date_str,earth_date_str)
        # 考虑时间流速比例
        time_ratio = settings['time_ratio']
        alien_days = delta_days * time_ratio*24/settings['rotation']
        # 计算外星年的月和日
        alien_year_days = settings['orbital']
        alien_month_days = settings['month_days']
        alien_year = alien_days // alien_year_days
        alien_days_in_year = alien_days % alien_year_days
        alien_month = alien_days_in_year // alien_month_days
        alien_day = alien_days_in_year % alien_month_days
        # 显示转换后的外星日期
        self.line_edit_alien_date.setText(f"{int(alien_year)+1:02d}-{int(alien_month)+1:02d}-{int(alien_day)+1:02d}"
)
    def convert_alien_to_earth(self):
        # 获取外星日期输入
        lst = self.line_edit_alien_date.text().split('-')
        alien_year = int(lst[0])
        alien_month = int(lst[1])
        alien_day = int(lst[2])
        # 获取用户设置
        settings = self.settings
        if not settings:
            print("Error: Settings not loaded.")
            return
        # 计算外星年的总天数
        alien_year_days = settings['orbital']
        alien_month_days = settings['month_days']
        alien_total_days = (alien_year-1) * (alien_year_days-1) + (alien_month-1) * alien_month_days + alien_day-1
        # 考虑时间流速比例
        time_ratio = settings['time_ratio']
        total_days = alien_total_days / time_ratio
        # 计算地球日期
        date_after_addition =  settings['epoch'] + timedelta(days=total_days)
        # 显示转换后的地球日期
        self.line_edit_earth_date.setText(date_after_addition.strftime("%Y-%m-%d"))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.load_settings()  # 加载设置
    main_window.show()
    sys.exit(app.exec())

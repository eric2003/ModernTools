import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

def convert_path():
    path = entry.text()
    converted_path = re.sub(r'\\', '/', path)
    QMessageBox.information(window, "转换结果", f"转换后的路径为：\n{converted_path}")

# 创建应用
app = QApplication([])

# 创建窗口
window = QWidget()
window.setWindowTitle("路径转换器")

# 创建布局
layout = QVBoxLayout()

# 创建输入框
entry = QLineEdit()
entry.setPlaceholderText("请输入路径")
layout.addWidget(entry)

# 创建按钮
convert_button = QPushButton("转换路径")
convert_button.clicked.connect(convert_path)
layout.addWidget(convert_button)

# 设置布局
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用
app.exec()
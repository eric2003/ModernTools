import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from PyQt6.QtGui import QGuiApplication

def convert_path():
    path = entry.text()
    converted_path = re.sub(r'\\', '/', path)
    output_label.setText(f"转换后的路径为：\n{converted_path}")

def copy_path():
    converted_path = output_label.text()
    # 检查是否包含换行符
    parts = converted_path.split('\n', 1)
    if len(parts) > 1:
        path_to_copy = parts[1]  # 获取换行符之后的部分
    else:
        path_to_copy = converted_path  # 如果没有换行符，直接复制整个内容
    clipboard = QGuiApplication.clipboard()
    clipboard.setText(path_to_copy)
    QMessageBox.information(window, "复制成功", "路径已复制到剪贴板！")

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

# 创建输出标签
output_label = QLabel("转换后的路径将显示在这里")
output_label.setWordWrap(True)  # 允许自动换行
layout.addWidget(output_label)

# 创建复制按钮
copy_button = QPushButton("复制路径")
copy_button.clicked.connect(copy_path)
layout.addWidget(copy_button)

# 设置布局
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用
app.exec()
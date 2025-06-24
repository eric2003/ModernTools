import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from PyQt6.QtCore import Qt
import chardet
import codecs

class EncodingDetectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件编码检测器")
        self.setFixedSize(500, 350)

        # 创建主窗口部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 标题标签
        title_label = QLabel("文件编码检测器")
        title_label.setStyleSheet("font-size: 14pt; font-family: Arial; font-weight: bold;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # 选择文件按钮
        select_button = QPushButton("选择文件")
        select_button.setStyleSheet("font-size: 10pt; font-family: Arial; padding: 5px;")
        select_button.clicked.connect(self.detect_encoding)
        main_layout.addWidget(select_button)

        # 结果文本框（可复制）
        self.result_field = QTextEdit()
        self.result_field.setFixedHeight(120)
        self.result_field.setStyleSheet("font-size: 10pt; font-family: Arial; background-color: #ffffff; border: 1px solid #ddd;")
        self.result_field.setText("请选择一个文件以检测其编码")
        self.result_field.setReadOnly(False)  # 允许复制
        main_layout.addWidget(self.result_field)

        # 添加拉伸以保持布局整洁
        main_layout.addStretch()

        # 设置窗口背景
        self.setStyleSheet("background-color: #f0f0f0;")

    def detect_encoding(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if not file_path:
            self.result_field.setText("未选择文件")
            return

        try:
            # 使用 chardet 检测编码
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                chardet_result = chardet.detect(raw_data)
                encoding = chardet_result['encoding']
                confidence = chardet_result['confidence']

            # 检查是否为 UTF-8-BOM
            bom_utf8 = codecs.BOM_UTF8
            if raw_data.startswith(bom_utf8):
                encoding = "UTF-8-BOM"

            # 检查是否为 ANSI (假设 Windows 默认 CP1252)
            if encoding is None or encoding.lower() == 'ascii':
                try:
                    with open(file_path, 'r', encoding='cp1252') as file:
                        file.read()
                    encoding = "ANSI (CP1252)"
                except UnicodeDecodeError:
                    encoding = "未知编码"

            # 显示结果
            result_text = f"文件: {file_path}\n编码: {encoding}\n置信度: {confidence:.2%}"
            self.result_field.setText(result_text)

        except Exception as e:
            self.result_field.setText(f"错误: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EncodingDetectorWindow()
    window.show()
    sys.exit(app.exec())
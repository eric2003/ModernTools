import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from PyQt6.QtCore import Qt
import chardet
import codecs
from collections import Counter

class DirectoryEncodingDetectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("目录文件编码检测器")
        self.setFixedSize(600, 500)

        # 创建主窗口部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 标题标签
        title_label = QLabel("目录文件编码检测器")
        title_label.setStyleSheet("font-size: 14pt; font-family: Arial; font-weight: bold;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # 选择目录按钮
        select_button = QPushButton("选择目录")
        select_button.setStyleSheet("font-size: 10pt; font-family: Arial; padding: 5px;")
        select_button.clicked.connect(self.detect_directory_encoding)
        main_layout.addWidget(select_button)

        # 编码统计文本框（可复制）
        self.stats_field = QTextEdit()
        self.stats_field.setFixedHeight(150)
        self.stats_field.setStyleSheet("font-size: 10pt; font-family: Arial; background-color: #ffffff;Edit; border: 1px solid #ddd;")
        self.stats_field.setText("请选择一个目录以检测其文件编码")
        self.stats_field.setReadOnly(False)  # 允许复制
        main_layout.addWidget(self.stats_field)

        # 非主流编码文件标签
        minority_label = QLabel("非主流编码文件：")
        minority_label.setStyleSheet("font-size: 12pt; font-family: Arial;")
        main_layout.addWidget(minority_label)

        # 非主流编码文件列表文本框（可复制）
        self.minority_field = QTextEdit()
        self.minority_field.setStyleSheet("font-size: 10pt; font-family: Arial; background-color: #ffffff; border: 1px solid #ddd;")
        self.minority_field.setText("非主流编码文件将显示在这里")
        self.minority_field.setReadOnly(False)  # 允许复制
        main_layout.addWidget(self.minority_field)

        # 设置窗口背景
        self.setStyleSheet("background-color: #f0f0f0;")

    def detect_directory_encoding(self):
        directory = QFileDialog.getExistingDirectory(self, "选择目录")
        if not directory:
            self.stats_field.setText("未选择目录")
            self.minority_field.setText("未选择目录")
            return

        try:
            # 收集所有文件的编码
            encoding_counts = Counter()
            total_files = 0
            minority_files = []
            file_list = []

            # 递归遍历目录
            for root, _, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'rb') as file:
                            raw_data = file.read()
                            if not raw_data:  # 跳过空文件
                                continue
                            chardet_result = chardet.detect(raw_data)
                            encoding = chardet_result['encoding']
                            confidence = chardet_result['confidence']

                            # 检查 UTF-8-BOM
                            bom_utf8 = codecs.BOM_UTF8
                            if raw_data.startswith(bom_utf8):
                                encoding = "UTF-8-BOM"

                            # 检查 ANSI (假设 CP1252)
                            if encoding is None or encoding.lower() == 'ascii':
                                try:
                                    with open(file_path, 'r', encoding='cp1252') as file:
                                        file.read()
                                    encoding = "ANSI (CP1252)"
                                except UnicodeDecodeError:
                                    encoding = "未知编码"

                            encoding_counts[encoding] = encoding_counts.get(encoding, 0) + 1
                            total_files += 1
                            file_list.append((file_path, encoding))

                    except Exception as e:
                        encoding_counts["错误"] = encoding_counts.get("错误", 0) + 1
                        total_files += 1
                        file_list.append((file_path, "错误"))

            if total_files == 0:
                self.stats_field.setText("目录中没有文件")
                self.minority_field.setText("无非主流编码文件")
                return

            # 确定主流编码（出现次数最多的编码）
            most_common_encoding = encoding_counts.most_common(1)[0][0] if encoding_counts else "未知编码"

            # 生成统计结果
            stats_text = f"目录: {directory}\n总文件数: {total_files}\n\n编码统计:\n"
            for encoding, count in encoding_counts.items():
                percentage = (count / total_files) * 100
                stats_text += f"{encoding}: {count} 个文件 ({percentage:.2f}%)\n"

            # 找出非主流编码文件
            minority_files = [f"{file_path} ({encoding})" for file_path, encoding in file_list if encoding != most_common_encoding and encoding != "错误"]
            minority_text = "\n".join(minority_files) if minority_files else "无非主流编码文件"

            # 显示结果
            self.stats_field.setText(stats_text.strip())
            self.minority_field.setText(minority_text)

        except Exception as e:
            self.stats_field.setText(f"错误: {str(e)}")
            self.minority_field.setText("错误发生，无法列出非主流编码文件")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DirectoryEncodingDetectorWindow()
    window.show()
    sys.exit(app.exec())
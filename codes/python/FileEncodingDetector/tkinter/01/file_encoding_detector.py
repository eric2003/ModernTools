import tkinter as tk
from tkinter import ttk, filedialog
import chardet
import codecs

def detect_encoding():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_path:
        result_field.delete("1.0", tk.END)
        result_field.insert("1.0", "No file selected")
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
                encoding = "Unknown"

        # 显示结果
        result_text = f"File: {file_path}\nEncoding: {encoding}\nConfidence: {confidence:.2%}"
        result_field.delete("1.0", tk.END)
        result_field.insert("1.0", result_text)

    except Exception as e:
        result_field.delete("1.0", tk.END)
        result_field.insert("1.0", f"Error: {str(e)}")

# 创建主窗口
root = tk.Tk()
root.title("File Encoding Detector")
root.geometry("500x350")
root.configure(bg="#f0f0f0")

# 创建主框架
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill="both")

# 标题标签
title_label = ttk.Label(main_frame, text="File Encoding Detector", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# 选择文件按钮
select_button = ttk.Button(main_frame, text="Select File", command=detect_encoding)
select_button.pack(pady=10)

# 结果文本框（可复制）
result_field = tk.Text(main_frame, height=8, width=50, font=("Arial", 10), wrap="word", relief="solid", background="#ffffff")
result_field.insert("1.0", "Select a file to detect its encoding")
result_field.pack(pady=10, padx=10, fill="both", expand=True)

# 启动主循环
root.mainloop()
import tkinter as tk
from tkinter import ttk

def to_upper_case():
    input_text = input_field.get("1.0", tk.END).strip()
    result_field.delete("1.0", tk.END)
    result_field.insert("1.0", input_text.upper())

def to_lower_case():
    input_text = input_field.get("1.0", tk.END).strip()
    result_field.delete("1.0", tk.END)
    result_field.insert("1.0", input_text.lower())

# 创建主窗口
root = tk.Tk()
root.title("String Case Converter")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# 创建主框架
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

# 输入标签
input_label = ttk.Label(main_frame, text="Enter Text:", font=("Arial", 12))
input_label.pack(anchor="w")

# 输入文本框
input_field = tk.Text(main_frame, height=5, width=40, font=("Arial", 10))
input_field.pack(pady=10)

# 按钮框架
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

# 大写按钮
upper_button = ttk.Button(button_frame, text="To Upper Case", command=to_upper_case)
upper_button.pack(side=tk.LEFT, padx=5)

# 小写按钮
lower_button = ttk.Button(button_frame, text="To Lower Case", command=to_lower_case)
lower_button.pack(side=tk.LEFT, padx=5)

# 结果文本框（可复制）
result_field = tk.Text(main_frame, height=5, width=40, font=("Arial", 10), wrap="word", relief="solid", background="#ffffff")
result_field.insert("1.0", "Result will appear here")
result_field.pack(pady=20)

# 启动主循环
root.mainloop()
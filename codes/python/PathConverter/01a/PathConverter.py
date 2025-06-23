import re

# 提示用户输入原始路径
path = input("请输入原始路径（例如：d:\\work\\vtk_2024_work\\ModernVTK\\）：")

# 替换反斜杠为正斜杠
converted_path = re.sub(r'\\', '/', path)

print(converted_path)
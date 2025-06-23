import re

# 原始路径
path = "d:\\work\\vtk_2024_work\\ModernVTK\\"

# 替换反斜杠为正斜杠
converted_path = re.sub(r'\\', '/', path)

print(converted_path)
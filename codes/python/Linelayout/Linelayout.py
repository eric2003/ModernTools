# 定义文件路径
file_path = 'my.txt'  # 替换为你的文件路径

# 打开文件并读取内容
with open(file_path, 'r') as file:
    lines = file.readlines()

# 移除空行
lines = [line.strip() for line in lines if line.strip()]

# 按分号分割内容
entries = [entry.split(';') for entry in lines if ';' in entry]

# 遍历所有条目并打印
for entry in entries:
    for file_path in entry:
        print(file_path.strip())
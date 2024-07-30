import os

def count_lines_in_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return sum(1 for line in file if line.strip())

def count_lines_in_directory(directory):
    total_lines = 0
    _, _, files = next(os.walk(directory))  # 只获取当前目录下的文件
    for file in files:
        if file.endswith('.py'):  # 修改这里的扩展名以适应你的需求
            filepath = os.path.join(directory, file)
            total_lines += count_lines_in_file(filepath)
    return total_lines

directory_path = 'E:/develop/context/arm/strategy'  # 修改为你的项目目录
total_lines = count_lines_in_directory(directory_path)
print(f'Total lines of code: {total_lines}')
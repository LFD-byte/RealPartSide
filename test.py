import os
def saveFile():
    path = 'D:/code/Python/Class_GraduationProject/RealPartSide/demo2.dialog'
    data = [{'1': 2}, {'1': 2}]
    # 文件是否已存在
    if os.path.isfile(path):
        print("警告", "文件已存在")
    # 创建新文件
    else:
        pathList = []
        if '\\' in path:
            pathList = path.split('\\')
        elif '/' in path:
            pathList = path.split('/')
        print('/'.join(pathList[:-1]))
        if os.path.isdir('/'.join(pathList[:-1])):
            with open(path, 'w', encoding="utf-8") as f:
                for i in range(len(data)):
                    f.write(str((data[i])) + '\n')

saveFile()
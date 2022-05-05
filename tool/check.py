import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(FILE_PATH, '../source')

def start():
    fileList = []
    temp = os.listdir(SOURCE_PATH)
    for f in temp:
        if f[-4:] == '.svg':
            fileList.append(os.path.splitext(f)[0])
    temp = None
    print("SVG source file: %d" % len(fileList))

    n = 0
    with open(os.path.join(FILE_PATH, '国标一级汉字.txt'), 'r', encoding='utf-8') as f:
        list = f.read()
    for c in list:
        if c in fileList:
            n += 1
    print("国标一级汉字 %d/%d" % (n, len(list)))
        
    n = 0
    with open(os.path.join(FILE_PATH, '国标二级汉字.txt'), 'r', encoding='utf-8') as f:
        list = f.read()
    for c in list:
        if c in fileList:
            n += 1
    print("国标二级汉字 %d/%d" % (n, len(list)))
    
    with open(os.path.join(FILE_PATH, 'glyphList.txt'), 'w', encoding='utf-8') as tFile:
        glyphNameList = str()
        fileList.sort()
        for c in fileList:
            if c.isdecimal():
                glyphNameList += chr(int(c))
            else:
                glyphNameList += c

        tFile.write(glyphNameList)

start()
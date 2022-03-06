import os

def start():
    fileList = set()
    temp = os.listdir('../svg/source')
    for f in temp:
        if f[-4:] == '.svg':
            fileList.add(os.path.splitext(f)[0])
    temp = None
    print("SVG source file: %d" % len(fileList))

    n = 0
    with open('国标一级汉字.txt', 'r') as f:
        list = f.read()
    for c in list:
        if c in fileList:
            n += 1
    print("国标一级汉字 %d/%d" % (n, len(list)))
        
    n = 0
    with open('国标二级汉字.txt', 'r') as f:
        list = f.read()
    for c in list:
        if c in fileList:
            n += 1
    print("国标二级汉字 %d/%d" % (n, len(list)))

start()
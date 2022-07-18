import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(FILE_PATH)
TEMP_TASK_PATH = os.path.join(FILE_PATH, 'tmp')
COMP_PATH =  os.path.join(PROJECT_PATH, 'components')

def genCompGlyph():
    JIEGOU_PATH = os.path.join(PROJECT_PATH, 'hanzi-jiegou')
    if not os.path.exists(JIEGOU_PATH):
        print('Not found hanzi-jiegou')
        return

    import sys
    sys.path.append(os.path.join(JIEGOU_PATH, 'scripts'))
    import genGlyphTab as gen

    filePath = 'glyph.json'
    
    oldFiles = set()
    for filename in os.listdir(TEMP_TASK_PATH):
        if(filename[-4:] == '.svg'):
            oldFiles.add(filename)
            
    gen.genGlyphTab(filePath)
    newFiles = gen.genGlyphFiles(TEMP_TASK_PATH, filePath)
    
    if not os.path.exists(COMP_PATH):
        os.mkdir(COMP_PATH)
    compFiles = set(os.listdir(COMP_PATH))
    rFile = oldFiles - newFiles
    reFile = compFiles - newFiles

    print('删除%d个旧文件' % len(rFile))
    print('添加%d个新文件' % len(newFiles - oldFiles - compFiles))
    print('%d个组件不需要' % len(reFile))
    if len(reFile): print(reFile)

    for file in rFile: os.remove(os.path.join(TEMP_TASK_PATH, file))
    for file in compFiles - reFile: os.remove(os.path.join(TEMP_TASK_PATH, file))

    
if __name__ == '__main__':
    genCompGlyph()
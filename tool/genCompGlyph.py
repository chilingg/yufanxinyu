import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(FILE_PATH)
TEMP_TASK_PATH = os.path.join(FILE_PATH, 'tmp')

def genCompGlyph():
    JIEGOU_PATH = os.path.join(PROJECT_PATH, 'hanzi-jiegou')
    if not os.path.exists(JIEGOU_PATH):
        print('Not found hanzi-jiegou')
        return

    import sys
    sys.path.append(os.path.join(JIEGOU_PATH, 'scripts'))
    import genGlyphTab as gen

    filePath = os.path.join(FILE_PATH, 'glyph.json')
    gen.genGlyphTab(filePath)
    gen.genGlyphFiles(TEMP_TASK_PATH, filePath)
    
genCompGlyph()
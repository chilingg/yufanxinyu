import os
import sys
import json
import re

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
COMP_PATH = os.path.join(PROJECT_PATH, 'components')
SYMBOL_PATH = os.path.join(PROJECT_PATH, 'symbol')
TEMP_GLYPH_FILE = 'tempGlyph.svg'
FONT_FILE_PATH = os.path.join(PROJECT_PATH, 'font')

FONT_WIDTH = 720
LITTLE_F_WIDTH = 360

def loadJson(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def start():
    if not os.path.exists(FONT_FILE_PATH):
        os.mkdir(FONT_FILE_PATH)

    if os.path.exists('clsvg'):
        sys.path.append('clsvg')
        
    if not os.path.exists('glyph.json'):
        JIEGOU_PATH = os.path.join(PROJECT_PATH, 'hanzi-jiegou')
        if not os.path.exists(JIEGOU_PATH):
            raise Exception('Not found <glyph.json> and <hanzi-jiegou>!')
        sys.path.append(os.path.join(JIEGOU_PATH, 'scripts'))
        import genGlyphTab
        genGlyphTab.genGlyphTab('glyph.json')

def finish():
    if os.path.exists(TEMP_GLYPH_FILE):
        os.remove(TEMP_GLYPH_FILE)

def writeTempGlyphFromShape(shape, tag, attrib):
    newRoot = svgfile.ET.Element(tag, attrib)
    newRoot.text = '\n'
    styleElem = svgfile.ET.Element('style', { 'type': 'text/css' })
    styleElem.text = '.st0{fill:#000000;}'
    styleElem.tail = '\n'
    newRoot.append(styleElem)

    newRoot.append(shape.toSvgElement({ 'class': 'st0' }))
    newTree = svgfile.ET.ElementTree(newRoot)
    newTree.write(TEMP_GLYPH_FILE, encoding = "utf-8", xml_declaration = True)

def genGroupFromPath(filepath, strokeWidth):
    tree = svgfile.parse(filepath)
    root = tree.getroot()

    g = bezierShape.GroupShape()
    for child in root:
        tag = svgfile.unPrefix(child.tag)
        if tag != 'style':
            paths = bezierShape.createPathfromSvgElem(child, tag)
            if len(paths):
                shape = bezierShape.BezierShape()
                shape.extend(paths[0].toOutline(strokeWidth, 'Round', 'Round'))
                g |= bezierShape.GroupShape(shape)
    return g

def importGlyph(sfdFile, strokeWidth):
    GLYPH_TAG = 'svg'
    GLYPH_ATTRIB = {
        'version': '1.1',
        'id': 'glyph',
        'x': '0px',
        'y': '0px',
        'viewBox': '0 0 720 900',
        'style': 'enable-background:new 0 0 720 900;',
        'space': 'preserve'
        }

    glyphTable = loadJson(os.path.join(PROJECT_PATH, 'glyph.json'))
    charsList = {}
    errorList = {}

    fileList = os.listdir(COMP_PATH)
    num = len(fileList)
    count = 0
    for comp, fmts in glyphTable.items():
        for fmt, chars in fmts.items():
            fileName = '%s：%s.svg' % (comp, fmt)
            fileName = re.sub('>', '》',  '%s：%s.svg' % (comp, fmt))
            if fileName not in fileList:
                continue

            count += 1
            print('(%d/%d)Process %s ...' % (count, len(fileList), fileName))

            try:
                g = genGroupFromPath(os.path.join(COMP_PATH, fileName), strokeWidth)
            except Exception as e:
                errorList[fileName] = e
                print(fileName + ' is error!')

            for char in chars:
                if char not in charsList:
                    charsList[char] = bezierShape.GroupShape()
                if char not in errorList:
                    try:
                        charsList[char] |= g
                    except Exception as e:
                        errorList[char] = e
                        print(char + ' is error!')

    font = fontforge.open(sfdFile)
    font.selection.all()
    #font.clear()
    font.createChar(32).width = LITTLE_F_WIDTH #空格

    count = 0
    num = len(charsList)
    for char, glyphGroup in charsList.items():
        count += 1
        code = ord(char)
        width = FONT_WIDTH

        print("(%d/%d)%s: import glyph '%s' %d from %s" % (count, num, font.fontname, char, code, char))
        writeTempGlyphFromShape(glyphGroup.toShape(), GLYPH_TAG, GLYPH_ATTRIB)

        glyph = font.createChar(code)
        glyph.importOutlines(TEMP_GLYPH_FILE)
        glyph.width = width

    fileList = os.listdir(SYMBOL_PATH)
    count = 0
    sNum = len(fileList)
    for filename in fileList:
        if(filename[-4:] == '.svg'):
            char = filename[0]
            code = ord(char)
            width = FONT_WIDTH
            count += 1

            if(filename[:-4].isdecimal()):
                n = int(filename[:-4])
                if(n < 128):
                    code = n
                    char = chr(code)
                    if(code != 64):
                        width = LITTLE_F_WIDTH
                    sNum += 1

            print("(%d/%d)%s: import symbol glyph '%s' %d from %s" % (count, sNum, font.fontname, char, code, filename))
            
            try:
                g = genGroupFromPath(os.path.join(SYMBOL_PATH, filename), strokeWidth)
                writeTempGlyphFromShape(g.toShape(), GLYPH_TAG, GLYPH_ATTRIB)

                glyph = font.createChar(code)
                glyph.importOutlines(TEMP_GLYPH_FILE)
                glyph.width = width
            except Exception as e:
                errorList[filename] = e
                print(filename, e)
                #print(filename + ' is error!')

    print("%s: The Font has %d glyphs, of which %d are symbol" % (font.fontname, num, sNum))
    print("Generate font file in %s\n" % ("font/" + font.fontname + ".ttf"))
    font.generate(os.path.join(FONT_FILE_PATH, font.fontname + ".ttf"))
    #font.save()
    font.close()

    if len(errorList):
        for file, exp in errorList.items():
            print(file, exp)
        return -1
    else:
        return 0

if __name__ == '__main__':
    start()

    import fontforge
    from clsvg import svgfile
    from clsvg import bezierShape

    taskList = (
        ('YuFanXinYu-Bold.sfd', 48),
        ('YuFanXinYu-Medium.sfd', 39),
        ('YuFanXinYu-Regular.sfd', 30),
        ('YuFanXinYu-Light.sfd', 21)
        )

    for confFile, sWidth in taskList:
        if importGlyph(confFile, sWidth) == -1:
            break

    finish()
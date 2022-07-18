import os
import sys

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(FILE_PATH)
TEMP_FILE_PATH = os.path.join(PROJECT_PATH, 'components')
TEST_FILE_PATH = os.path.join(FILE_PATH, 'testGlyph')

def start():
    if not os.path.exists(TEST_FILE_PATH):
        os.mkdir(TEST_FILE_PATH)

    LIB = os.path.join(PROJECT_PATH, 'clsvg')
    if os.path.exists(LIB):
        sys.path.append(LIB)

start()

from clsvg import svgfile
from clsvg import bezierShape

import json
import re

def genGlyphFromPath(filepath, savePath, strokeWidth):
    tree = svgfile.parse(filepath)
    root = tree.getroot()

    newRoot = svgfile.ET.Element(root.tag, root.attrib)
    newRoot.text = '\n'
    styleElem = svgfile.ET.Element('style', { 'type': 'text/css' })
    styleElem.text = '.st0{fill:#000000;}'
    styleElem.tail = '\n'
    newRoot.append(styleElem)

    g = bezierShape.GroupShape()
    for child in root:
        tag = svgfile.unPrefix(child.tag)
        if tag != 'style':
            paths = bezierShape.createPathfromSvgElem(child, tag)
            if len(paths):
                shape = bezierShape.BezierShape()
                shape.extend(paths[0].toOutline(strokeWidth, 'Round', 'Round'))
                g |= bezierShape.GroupShape(shape)

    newRoot.append(g.toShape().toSvgElement({ 'class': 'st0' }))

    newTree = svgfile.ET.ElementTree(newRoot)
    newTree.write(savePath, encoding = "utf-8", xml_declaration = True)

def testGlyphGen():
    errorList = {}

    list = os.listdir(TEMP_FILE_PATH)
    #list.reverse()
    n = 0
    for filename in list:
        n += 1
        if(filename[-4:] == '.svg'):
            try:
                genGlyphFromPath(os.path.join(TEMP_FILE_PATH, filename), os.path.join(TEST_FILE_PATH, filename), 30)
                print('(%d/%d)%s ...' % (n, len(list), filename[:-4]))
            except Exception as e:
                errorList[filename[:-4]] = e
                print(filename[:-4] + ' is error!')

    if len(errorList):
        for file, exp in errorList.items():
            print(file, exp)

        return False
    else:
        return True

def testCharsGen():
    def loadJson(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)

    TEST_FILE_PATH = os.path.join(FILE_PATH, 'testChars')

    if not os.path.exists(TEST_FILE_PATH):
        os.mkdir(TEST_FILE_PATH)

    LIB = os.path.join(PROJECT_PATH, 'clsvg')
    if os.path.exists(LIB):
        sys.path.append(LIB)

    from clsvg import svgfile
    from clsvg import bezierShape

    compPath = os.path.join(FILE_PATH, 'testGlyph')
    fileList = os.listdir(compPath)
    charsList = {}
    glyphTable = loadJson(os.path.join(PROJECT_PATH, 'glyph.json'))
    # glyphTable = {
    #     "手": {
    #     "左右(1：2)0>扌": "扪"
    #     },
    #     "门": {
    #         "左右(1：2)1": "扪"
    #     },
    # }

    count = 0
    for comp, fmts in glyphTable.items():
        for fmt, chars in fmts.items():
            fileName = '%s：%s.svg' % (comp, fmt)
            fileName = re.sub('>', '》',  '%s：%s.svg' % (comp, fmt))
            if fileName not in fileList:
                continue
            else:
                count += 1
                print('(%d/%d)Process %s ...' % (count, len(fileList), fileName))

            tree = svgfile.parse(os.path.join(compPath, fileName))
            root = tree.getroot()

            shape = []
            for child in root:
                tag = svgfile.unPrefix(child.tag)
                if tag != 'style':
                    shape.append(bezierShape.createPathfromSvgElem(child, tag))

            for char in chars:
                if char not in charsList:
                    charsList[char] = []
                charsList[char].extend(shape)

    count = 0
    errorList = {}
    for char, shape in charsList.items():
        count += 1
        print('(%d/%d)Generating %s ...' % (count, len(charsList), char))

        newRoot = svgfile.ET.Element(root.tag, root.attrib)
        newRoot.text = '\n'
        styleElem = svgfile.ET.Element('style', { 'type': 'text/css' })
        styleElem.text = '.st0{fill:#ff5500;}'
        styleElem.tail = '\n'
        newRoot.append(styleElem)

        g = bezierShape.GroupShape()
        
        try:
            for path in shape:
                g |= bezierShape.GroupShape(path)
                
            newRoot.append(g.toShape().toSvgElement({ 'class': 'st0' }))
            newTree = svgfile.ET.ElementTree(newRoot)
            newTree.write(os.path.join(TEST_FILE_PATH, char + '.svg'), encoding = "utf-8", xml_declaration = True)
        except Exception as e:
            errorList[char] = e
            print(char + ' is error!')
        
    for file, exp in errorList.items():
        print(file, exp)

if __name__ == '__main__':
    # filename = '%s.svg' % '卣：单体'
    # genGlyphFromPath(os.path.join(TEMP_FILE_PATH, filename), os.path.join(TEST_FILE_PATH, filename), 30)

    if testGlyphGen():
        testCharsGen()
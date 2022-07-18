import os
import sys
import json
import re

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(FILE_PATH)

def checkChars():
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

    compPath = os.path.join(FILE_PATH, '../components')
    glyphTable = loadJson(os.path.join(PROJECT_PATH, 'glyph.json'))
    fileList = os.listdir(compPath)
    charsList = {}

    count = 0
    for comp, fmts in glyphTable.items():
        for fmt, chars in fmts.items():
            fileName = '%s：%s.svg' % (comp, fmt)
            fileName = re.sub('>', '》',  '%s：%s.svg' % (comp, fmt))
            if fileName not in fileList:
                continue
            else:
                count += 1
                #print('(%d/%d)Process %s ...' % (count, len(fileList), fileName))

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
    for char, shape in charsList.items():
        count += 1
        #print('(%d/%d)Generating %s ...' % (count, len(charsList), char))

        newRoot = svgfile.ET.Element(root.tag, root.attrib)
        newRoot.text = '\n'
        styleElem = svgfile.ET.Element('style', { 'type': 'text/css' })
        styleElem.text = '.st0{fill:none;stroke:#000000;stroke-width:48;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:10;}'
        styleElem.tail = '\n'
        newRoot.append(styleElem)
        for path in shape:
            newRoot.append(path.toSvgElement({ 'class': 'st0' }))
        newTree = svgfile.ET.ElementTree(newRoot)
        newTree.write(os.path.join(TEST_FILE_PATH, char + '.svg'), encoding = "utf-8", xml_declaration = True)

if __name__ == '__main__':
    checkChars()
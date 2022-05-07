import os
import sys

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
TEMP_FILE_PATH = os.path.join(FILE_PATH, 'tmp')
SOURCE_PATH = os.path.join(FILE_PATH, '../source')
TEST_FILE_PATH = os.path.join(FILE_PATH, 'testGlyph')
PROJECT_PATH = os.path.join(FILE_PATH, '../')

def start():
    if not os.path.exists(TEST_FILE_PATH):
        os.mkdir(TEST_FILE_PATH)

    LIB = os.path.join(PROJECT_PATH, 'clsvg')
    if os.path.exists(LIB):
        sys.path.append(LIB)

start()

from clsvg import svgfile
from clsvg import bezierShape

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
    list = os.listdir(TEMP_FILE_PATH)
    #list.reverse()
    for filename in list:
        if(filename[-4:] == '.svg'):
            print(filename[:-4] + ' ...')

            genGlyphFromPath(os.path.join(TEMP_FILE_PATH, filename), os.path.join(TEST_FILE_PATH, filename), 30)

testGlyphGen()
#filename = '%s.svg' % '痹'
#genGlyphFromPath(os.path.join(SOURCE_PATH, filename), os.path.join(TEST_FILE_PATH, filename), 30)
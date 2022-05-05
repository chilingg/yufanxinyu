import os
import sys

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(FILE_PATH, 'source')
TEMP_GLYPH_FILE = 'tempGlyph.svg'
FONT_FILE_PATH = os.path.join(FILE_PATH, 'font')

def start():
    if not os.path.exists(FONT_FILE_PATH):
        os.mkdir(FONT_FILE_PATH)

    if os.path.exists('clsvg'):
        sys.path.append('clsvg')

def finish():
    if os.path.exists(TEMP_GLYPH_FILE):
        os.remove(TEMP_GLYPH_FILE)

start()

import fontforge
from clsvg import svgfile
from clsvg import bezierShape

FONT_WIDTH = 720
LITTLE_F_WIDTH = 360

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
            shape = bezierShape.BezierShape()
            shape.extend(bezierShape.createPathfromSvgElem(child, tag)[0].toOutline(strokeWidth, 'Round', 'Round'))
            g |= bezierShape.GroupShape(shape)

    newRoot.append(g.toShape().toSvgElement({ 'class': 'st0' }))

    newTree = svgfile.ET.ElementTree(newRoot)
    newTree.write(savePath, encoding = "utf-8", xml_declaration = True)

def importGlyph(sfdFile, strokeWidth):
    font = fontforge.open(sfdFile)
    font.selection.all()
    font.clear()
    font.createChar(32).width = LITTLE_F_WIDTH #空格

    num = 0
    ascii = 0

    list = os.listdir(SOURCE_PATH)
    for filename in list:
        if(filename[-4:] == '.svg'):
            char = filename[0]
            code = ord(char)
            width = FONT_WIDTH

            if(filename[:-4].isdecimal()):
                n = int(filename[:-4])
                if(n < 128):
                    code = n
                    char = chr(code)
                    if(code != 64):
                        width = LITTLE_F_WIDTH
                    ascii += 1

            print("%s: import glyph '%s' %d from %s" % (font.fontname, char, code, filename))
            genGlyphFromPath(os.path.join(SOURCE_PATH, filename), TEMP_GLYPH_FILE, strokeWidth)

            glyph = font.createChar(code)
            glyph.importOutlines(TEMP_GLYPH_FILE)
            glyph.width = width
            num += 1

    print("%s: The Font has %d glyphs, of which %d are ASCII" % (font.fontname, num, ascii))
    print("Generate font file in %s\n" % ("font/" + font.fontname + ".ttf"))
    font.generate(os.path.join(FONT_FILE_PATH, font.fontname + ".ttf"))
    font.save()
    font.close()

importGlyph('YuFanXinYu-Bold.sfd', 50)
importGlyph('YuFanXinYu-Medium.sfd', 40)
importGlyph('YuFanXinYu-Regular.sfd', 30)
importGlyph('YuFanXinYu-Light.sfd', 20)

finish()
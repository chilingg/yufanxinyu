import os
import fontforge

FONT_WIDTH = 720
LITTLE_F_WIDTH = 360

def start():
    if os.path.exists('font'):
        return
    else:
        os.mkdir('font')

def importGlyph(path, file):
    font = fontforge.open(file)
    font.selection.all()
    font.clear()
    font.createChar(32).width = LITTLE_F_WIDTH

    num = 0
    ascii = 0

    list = os.listdir(path)
    for filename in list:
        if(filename[-4:] == '.svg'):
            char = filename[0]
            code = ord(char)
            filepath = "%s/%s" % (path, filename)
            width = FONT_WIDTH

            if(filename[:-4].isdecimal()):
                n = int(filename[:-4])
                if(n < 128):
                    code = n
                    char = chr(code)
                    if(code != 64):
                        width = LITTLE_F_WIDTH
                    ascii += 1

            print("%s: import glyph '%s' %d from %s" % (font.fontname, char, code, filepath))

            glyph = font.createChar(code)
            glyph.importOutlines(filepath)
            glyph.width = width
            num += 1

    print("%s: The Font has %d glyphs, of which %d are ASCII" % (font.fontname, num, ascii))
    print("Generate font file in %s\n" % ("font/" + font.fontname + ".ttf"))
    font.generate("font/" + font.fontname + ".ttf")
    font.save()
    font.close()

start()
importGlyph('svg/bold', 'YuFanXinYu-Bold.sfd')
importGlyph('svg/regular', 'YuFanXinYu-Regular.sfd')
importGlyph('svg/light', 'YuFanXinYu-Light.sfd')
importGlyph('svg/medium', 'YuFanXinYu-Medium.sfd')
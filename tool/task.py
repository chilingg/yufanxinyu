import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(FILE_PATH, '../source')
TEMP_TASK_PATH = os.path.join(FILE_PATH, 'tmp')

def start():
    if not os.path.exists(TEMP_TASK_PATH):
        os.mkdir(TEMP_TASK_PATH)

    with open(os.path.join(FILE_PATH, '国标一级汉字.txt'), 'r', encoding='utf-8') as f:
        list = f.read()
        f.close()

        n = 0
        for c in list:
            if not os.path.exists(os.path.join(SOURCE_PATH, "%s.svg" % c)):
                tFile = open(os.path.join(TEMP_TASK_PATH, '%s.svg' % c), "w")
                tFile.close()
                n += 1
            if n == 100:
                break
    
start()
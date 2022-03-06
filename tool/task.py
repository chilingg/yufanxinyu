import os

def start():
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    with open('国标一级汉字.txt', 'r') as f:
        list = f.read()
        f.close()

        n = 0
        for c in list:
            if(not os.path.exists("../svg/source/%s.svg" % c)):
                tFile = open('tmp/%s.svg' % c, "w")
                tFile.close()
                n += 1
            if(n == 100):
                break
    
start()
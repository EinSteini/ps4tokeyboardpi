NULL_CHAR = chr(0)

def ms_write(report):
    with open("/dev/hidg1", "rb+") as fd:
        print(fd.write(report.encode()))

ms_write(NULL_CHAR+chr(100)+chr(100))
ms_write(chr(2)+NULL_CHAR*2)
ms_write(NULL_CHAR*3)
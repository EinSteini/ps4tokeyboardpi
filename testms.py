def ms_write(report):
    with open("/dev/hidg1", "rb+") as fd:
        print(fd.write(report))

ms_write(bytes([0,100,10]))
ms_write(bytes([1])+bytes(2))
ms_write(bytes(3))
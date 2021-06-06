
from pyPS4Controller.controller import Controller


NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_L3_up(self, a):
        print("W")
        write_report(NULL_CHAR*2+chr(26)+NULL_CHAR*5)

    def on_L3_down(self, a):
        print("S")
        write_report(NULL_CHAR*2+chr(22)+NULL_CHAR*5)

    def on_L3_left(self, a):
        print("A")
        write_report(NULL_CHAR*2+chr(4)+NULL_CHAR*5)

    def on_L3_right(self, a):
        print("D")
        write_report(NULL_CHAR*2+chr(7)+NULL_CHAR*5)

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60)

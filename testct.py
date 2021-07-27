from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_R3_up(self, a):
        print(f"y {int(a/256)}")

    def on_R3_down(self, a):
        print(f"y {int(a/256)}")

    def on_R3_left(self, a):
        print(f"x {int(a/256)}")
    
    def on_R3_right(self, a):
        print(f"x {int(a/256)}")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()

from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_L2_press(self, a):
        print("press")

    def on_L2_release(self):
        print("release")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()

from pyPS4Controller.controller import Controller
import time
import logging
import threading

NULL_CHAR = chr(0)

def write_kb(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def write_ms(report):
    with open('/dev/hidg1', 'rb+') as fd:
        fd.write(report.encode())


class InputStream():

    currentInputs = [False for i in range(8)]
    # [FW, L, B, R, J, C]

    def __init__(self):
        print("init stream")

    def getInputs(self):
        inputs = []

        for i in range(len(self.currentInputs)):
            if(self.currentInputs[i]):
                inputs.append(i)
        
        return inputs

    def input(self, input):
        if input == "FW":
            self.currentInputs[0] = self.currentInputs[0] != True
        elif input == "L":
           # print("L")
            self.currentInputs[1] = self.currentInputs[1] != True
        elif input == "B":
            #print("B")
            self.currentInputs[2] = self.currentInputs[2] != True
        elif input == "R":
            #print("R")
            self.currentInputs[3] = self.currentInputs[3] != True
        elif input == "J":
            #print("J")
            self.currentInputs[4] = self.currentInputs[4] != True
        elif input == "C":
            self.currentInputs[5] = self.currentInputs[5] != True
            
class MyController(Controller):

    input = InputStream()

    def __init__(self, **kwargs):
        print("init con")
        Controller.__init__(self, **kwargs)
        
    def getInputs(self):
        return self.input.getInputs()

    def on_L2_press(self, a):
        if 0 not in self.input.getInputs():
            self.input.input("FW")

    def on_L2_release(self):
        if 0 in self.input.getInputs():
            self.input.input("FW")

    def on_R2_press(self, a):
        if 2 not in self.input.getInputs():
            self.input.input("B")

    def on_R2_release(self):
        if 2 in self.input.getInputs():
            self.input.input("B")

    def on_L1_press(self):
        self.input.input("L")

    def on_L1_release(self):
        self.input.input("L")

    def on_R1_press(self):
        self.input.input("R")

    def on_R1_release(self):
        self.input.input("R")

    def on_x_press(self):
        self.input.input("J")

    def on_x_release(self):
        self.input.input("J")

    def on_down_arrow_press(self):
        self.input.input("C")

    def on_down_arrow_release(self):
        self.input.input("C")


def outputThread(name):
    logging.info("Thread %s: starting", name)

    stream = InputStream()
    sprint = True

    if(True):
        while(True):
            time.sleep(0.05)
            inputs = stream.getInputs()
            print(inputs)
                    
            if len(inputs) == 0:
                #print("interrupt")
                write_kb(NULL_CHAR*8)
            elif len(inputs) > 6:
                print("too many inputs")
                inputs = inputs[0::5]

            pressedKeys = NULL_CHAR*2
            if 0 in inputs:
                pressedKeys = chr(1) + NULL_CHAR
            if 5 in inputs:
                pressedKeys = chr(2) + NULL_CHAR

            iterator = 0

            for i in inputs:
                if iterator > 5:
                    break
                iterator += 1
                if i == 0:
                    print("W")
                    pressedKeys += chr(26)
                elif i == 1:
                    print("A")
                    pressedKeys += chr(4)
                elif i == 2:
                    print("S")
                    pressedKeys += chr(22)
                elif i == 3:
                    print("D")
                    pressedKeys += chr(7)
                elif i == 4:
                    print("JUMP")
                    pressedKeys += chr(44)
                else:
                    iterator -= 1

            print(pressedKeys)
            pressedKeys.replace("REPLACE", NULL_CHAR)
            print(pressedKeys)
            pressedKeys += NULL_CHAR*(6-iterator)

            write_kb(pressedKeys)

if __name__ == "__main__":
    time.sleep(1)
    format = "%(asctime)s: %(message)s"
    
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main  : creating OutputThread")

    x = threading.Thread(target=outputThread, args=("OutputThread",))
    x.start()
    
    logging.info("Main    : all done")

    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60)

    
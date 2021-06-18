from pyPS4Controller.controller import Controller
import time
import logging
import threading

NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


class InputStream():

    currentInputs = [False for i in range(6)]

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
        elif input == "IR":
            self.currentInputs[-1] = self.currentInputs[-1] != True
            

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

    def on_playstation_button_press(self):
        self.input.input("IN")

    def on_playstation_button_release(self):
        self.input.input("IN")

def outputThread(name):

    logging.info("Thread %s: starting", name)

    stream = InputStream()

    while(True):

            #time.sleep(0.05)

            inputs = stream.getInputs()
            print(inputs)
                    
            if len(inputs) == 0:
                print("interrupt")
                write_report(NULL_CHAR*8)

            for i in inputs:
                if i == 0:
                    #print("W")
                    write_report(NULL_CHAR*2+chr(26)+NULL_CHAR*5)
                if i == 1:
                    #print("A")
                    write_report(NULL_CHAR*2+chr(4)+NULL_CHAR*5)
                if i == 2:
                    #print("S")
                    write_report(NULL_CHAR*2+chr(22)+NULL_CHAR*5)
                if i == 3:
                    #print("D")
                    write_report(NULL_CHAR*2+chr(7)+NULL_CHAR*5)
                if i == 4:
                    #print("JUMP")
                    write_report(NULL_CHAR*2+chr(44)+NULL_CHAR*5)
                else:
                    write_report(NULL_CHAR*8)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main  : creating OutputThread")

    x = threading.Thread(target=outputThread, args=("OutputThread",))
    x.start()
    
    logging.info("Main    : all done")

    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60)

    
from pyPS4Controller.controller import Controller
import time
import logging
import threading

def write_kb(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report)

def write_ms(report):
    with open('/dev/hidg1', 'rb+') as fd:
        #print(f"mouse {report}")
        fd.write(report)


class InputStream():

    currentInputs = [False for i in range(8)]
    # [FW, L, B, R, J, C, LHB, RHB]

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
        elif input == "LHB":
            self.currentInputs[6] = self.currentInputs[6] != True
        elif input == "RHB":
            self.currentInputs[7] = self.currentInputs[7] != True
        
            
class MouseInput:
    
    #sensitivity = 1
    x = 0
    y = 0
    
    def __init__(self, sensitivity = 1):
        self.sensitivity = sensitivity if sensitivity <= 1 else 1 
    
    def input(self, x, y, btn = 0):
        self.x = x if x != 0 else self.x
        self.y = y if y != 0 else self.y
        btn = 0 if not btn else btn
        write_ms(bytes([btn, self.convertCoordinates(self.x), self.convertCoordinates(self.y)]))

    def reset(self):
        write_ms(bytes(3))

    def convertCoordinates(self, coord):
        result = int((coord/256)*self.sensitivity)
        if result < 0:
            result += 256

        return result



class MyController(Controller):

    input = InputStream()

    #Keyboard

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

    def on_share_press(self):
        self.input.input("LHB")

    def on_share_release(self):
        self.input.input("LHB")

    def on_options_press(self):
        self.input.input("RHB")

    def on_options_release(self):
        self.input.input("RHB")

    #Mouse

    mouse = MouseInput(0.4)

    def on_L3_up(self, a):
        self.mouse.input(0,a)

    def on_L3_down(self, a):
        self.mouse.input(0,a)

    def on_L3_left(self, a):
        self.mouse.input(a,0)
    
    def on_L3_right(self, a):
        self.mouse.input(a,0)
    
    def on_L3_x_at_rest(self):
        self.mouse.reset()

    def on_L3_y_at_rest(self):
        self.mouse.reset()

    def on_triangle_press(self):
        self.mouse.input(0,0,1)
    
    def on_triangle_release(self):
        self.mouse.input(0,0,0)

    def on_square_press(self):
        self.mouse.input(0,0,2)
    
    def on_square_release(self):
        self.mouse.input(0,0,0)    


def outputThread(name):
    logging.info("Thread %s: starting", name)

    stream = InputStream()
    currentHotbarPosition = 1

    if(True):
        while(True):
            time.sleep(0.05)
            inputs = stream.getInputs()
            print(inputs)
                    
            if len(inputs) == 0:
                #print("interrupt")
                write_kb(bytes(8))
            elif len(inputs) > 6:
                print("too many inputs")
                inputs = inputs[0::5]

            pressedKeys = bytes(2)
            if 0 in inputs:
                pressedKeys = bytes([1,0])
            if 5 in inputs:
                pressedKeys = bytes([2,0])

            iterator = 0

            for i in inputs:
                if iterator > 5:
                    break
                iterator += 1
                if i == 0:
                    print("W")
                    pressedKeys += bytes([26])
                elif i == 1:
                    print("A")
                    pressedKeys += bytes([4])
                elif i == 2:
                    print("S")
                    pressedKeys += bytes([22])
                elif i == 3:
                    print("D")
                    pressedKeys += bytes([7])
                elif i == 4:
                    print("JUMP")
                    pressedKeys += bytes([44])
                elif i == 6:
                    currentHotbarPosition = currentHotbarPosition - 1 if currentHotbarPosition > 1 else currentHotbarPosition
                    pressedKeys += bytes([29 + currentHotbarPosition])
                elif i == 7:
                    currentHotbarPosition = currentHotbarPosition + 1 if currentHotbarPosition < 9 else currentHotbarPosition
                    pressedKeys += bytes([29 + currentHotbarPosition])
                else:
                    iterator -= 1

            pressedKeys += bytes(6-iterator)
            print(pressedKeys)

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

    
import micropython # to enable disabling of accidental keyboard interrupt
from microbit import *
import radio
radio.config(group=23)

uart.init(baudrate=10000, bits=8, parity=None, stop=1, tx=None, rx=pin1)
micropython.kbd_intr(-1) # disable accidental keyboard interrupt, no idea if this works or is needed
dataList = []
delay = 250
capsLock = True
message = ''

keyCodes = {
  139: 'Q', 207: 'W', 210: 'E', 215: 'R', 150: 'T', 219: 'Y', 222: 'U', 161: 'I', 226: 'O', 231: 'P', 
  142: 'A', 205: 'S', 145: 'D', 213: 'F', 154: 'G', 217: 'H', 157: 'J', 224: 'K', 224: 'K', 229: 'L', 
  140: 'Z', 208: 'X', 209: 'C', 148: 'V', 152: 'B', 153: 'N', 220: 'M', 225: ',', 165: '.', 149: '_', 164: '?', 
  138: '1', 206: '2', 146: '3', 147: '4', 214: '5', 218: '6', 159: '7', 158: '8', 162: '9', 163: '0'
}

while True:
    if uart.any():
        data = bytearray(1)
        uart.readinto(data, 1)
        dataList.append(data[0])
        if len(dataList) == 3:
            if dataList[0] in keyCodes:
                if capsLock:
                    letter = keyCodes[dataList[0]]
                else:
                    letter = keyCodes[dataList[0]].lower()
                display.show(letter)
                message = message + letter
            elif dataList[0] == 172: # toggle caps lock
                capsLock = not capsLock
                if capsLock:
                    display.show(Image.ARROW_N)
                else:
                    display.show(Image.ARROW_S)
            elif dataList[0] == 242:
                display.show(Image.ARROW_W)
                message = message[:-1]
            elif dataList[0] == 131: # press F12 to review message
                display.scroll(message)
            elif dataList[0] == 236: # send message when enter pressed
                radio.on() 
                radio.send(message)
                radio.off()
                display.scroll('TX')
                message = ''
            dataList = []
            sleep(delay)
    display.clear()

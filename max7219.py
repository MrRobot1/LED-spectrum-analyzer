# Controll a max7219 LED driver with Raspberry pi

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)              # BCM = Gpio pin nr 
CLK = 11       #(23)
LATCH = 8      #(24)
data = 10      #(19)

GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(LATCH, GPIO.OUT)
GPIO.setup(data, GPIO.OUT)

GPIO.output(LATCH, 0)
GPIO.output(CLK, 0)




mapdictionary = { 0 : 0x00, 1 : 0x80, 2 : 0xC0, 3 : 0xE0, 4 : 0xF0, 5 : 0xF8, 6: 0xFC, 7: 0xFE, 8: 0xFF }            #0-8 antal lampar som ska lysa per rad (eller kolumn?)



def pattern(array):
    initMax7219()

    for i in range(1,9):
        address = i
        data = array[i-1]
        if((address >= 1) and (address<=8)):
            #print(address, "address", data, "data")
           
            writeToMax7219(address, data)



def freqToPattern(array):
    patternArray = [0] * len(array)
    for i in range(0, len(array)):
        
        patternArray[i] = mapdictionary[array[i]]

    return patternArray
        
    


def msbit(value):
    return value >> 7

def pulseCLK():
    GPIO.output(CLK, 1)
    time.sleep(0.00002)
    GPIO.output(CLK,0)
    return


def pulseCS():
    GPIO.output(LATCH, 1)
    time.sleep(0.001)
    GPIO.output(LATCH, 0)
    return


# shift byte into the max7219  MSB first
# 0x32  00110010
def insertByte(value):
    for x in range(0, 8):
        temp = value & 0x80
        msb = msbit(temp)            # most significant bit of byte
        GPIO.output(data, msb)
        pulseCLK()
        value = value << 1          # shift left



def writeToMax7219(address, data):
    insertByte(address)
    insertByte(data)
    pulseCS()
    return



def initMax7219():

    # set decode mode
    writeToMax7219(0x09, 0x00)  # no decode

    # set intensity 
    writeToMax7219(0x0A, 0x0D)

    # set scan limit 0-7 
    writeToMax7219(0x0B, 0x07)

    # set for normal operation
    writeToMax7219(0x0C, 0x01)

    # clear Max7219
    for x in range (1,9):
        writeToMax7219(x, 0x00)


    
    
    
    
  

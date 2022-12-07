#!/usr/bin/python
import RPi.GPIO as GPIO
from PIL import Image
import signal
import sys
from os import system


ledPin = 3
ledPinState = True

bombCounter = 0

interruptorPin = 37

def callbackSalir(senial, cuadro):
    '''Clear the GPIO pin and exits the program'''
    GPIO.cleanup()
    sys.exit(0)

def callbackInterruptor(canal):
    '''Turns the led on or off according to the last state.
    Also shows and image in the console'''
    global ledPinState
    global bombCounter
    if(ledPinState):
        ledPinState = False
        bombCounter += 1

        GPIO.output(ledPin, GPIO.HIGH)

        # If the number of times triggered is 4, then the bomb explodes and the programs ends 
        show_png(f"bomb_{bombCounter}.png")
        if (bombCounter >= 4 ): callbackSalir()
    else:
        ledPinState = True
        GPIO.output(ledPin, GPIO.LOW)

def show_png(imageName:str):
  '''Shows a png image in the console'''
  # Clear the console
  system("clear")
  # Try to open the image
  with Image.open(imageName) as im:
    # First load the image
    pix = im.load()

    # Then normalize the size to fit the console
    width, height = im.size
    finalWidth, finalHeight = 35, 30
    finalPixelWidth, finalPixelHeight = int(width/finalWidth), int(height/finalHeight)

    # Last, obtain the rgb values of the pixels and print it using ansii escape codes
    for y in range(finalHeight):
      for x in range(finalWidth):
        r,g,b = 0,0,0
        # Merging between pixels to fit the new image size
        for oX in range(finalPixelWidth):
          for oY in range(finalPixelHeight):
            oR,oG,oB,oA = pix[x*finalPixelWidth+oX,y*finalPixelHeight+oY]
            r += oR
            g += oG
            b += oB
            a += oA
        r = int (r / (finalPixelWidth * finalPixelHeight))
        g = int (g / (finalPixelWidth * finalPixelHeight))
        b = int (b / (finalPixelWidth * finalPixelHeight))
        a = int (a / (finalPixelWidth * finalPixelHeight))
        print(f'\033[48;2;{r};{g};{b}m', end= '  ')
      print('\033[0m',end='\n')

    # Remove the following lines to debug
    # print( f'Width: {width}; Terminal{finalWidth}; Pixel {finalPixelWidth}')
    # print( f'Height: {height}; Terminal{finalHeight}; Pixel {finalPixelHeight}')

def main():

    system("clear")

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(interruptorPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.add_event_detect(interruptorPin, GPIO.BOTH,callback=callbackInterruptor, bouncetime=5)
    signal.signal(signal.SIGINT, callbackSalir)
    signal.pause()
                  

if __name__ == '__main__':          
  main()

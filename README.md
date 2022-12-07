# P6-ReedSwitch
## Hardware problems
Not as much problems as in the previous exercices, but still the magnet was missing in our kit.

## Observations
The code is really similar to the one in excercise 3, because the behaviours are almost the same.

We used a normal led instead of a rgb one because it doesn't matter as much as in the previous excercise.
The led turns on when the switch is enabled and off when not.
```python
GPIO.setup(ledPin, GPIO.OUT)
```

An extra feature thet we decided to add is the display in the terminal of some images. This is accomplished using the PIL library ( that you need to have installed ) and then extracting the rgba values of each pixel from the image.
```python
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
```

When triggered four times the bomb will explote and the program will exit.
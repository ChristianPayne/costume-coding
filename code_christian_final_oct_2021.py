import time
import board
import neopixel
import math
import random

pixel_pin = board.D24
# num_pixels = 19 + 12
# num_pixels = 38
num_pixels = 6

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=(1, 0, 2))

PURPLE = (75,0,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0, 0, 255)
ORANGE = (255, 40, 0)
NEON_GREEN = (255, 255, 0)
YELLOW = (255, 180, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
PINK = (255, 0, 255)

ALL_COLORS = [RED, GREEN, BLUE, ORANGE, NEON_GREEN, YELLOW, CYAN, WHITE]

COLOR = PURPLE

 
def grad(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (0, pos * 3, 255)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, 255)
    pos -= 170
    return (0, 0, 255)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def chase (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    tailLength = 3
    dotColor = (255, 255, 255)
    tailColor = (0, 255, 0)

    framePercent = frameNumber / totalFrames

    pixels.fill((0,255,255))
    # if(frameNumber == 0):
    #     for pixel in pixelGroup:
    #         pixels[pixel] = (0,0,0)
    for pixel in range(len(pixelGroup)):
        if(pixel == int(framePercent * len(pixelGroup))):
            pixels[pixelGroup[pixel]] = dotColor
            for i in range(tailLength):
                pixels[pixelGroup[pixel - i - 1]] = tailColor
        # else:
        #     pixels[pixelGroup[pixel]] = (0, 0, 0)

def glitch(frameNumber: int, pixelGroup: list[int], totalFrames: int):
    randomPixelRange = pixelGroup[
            random.randint(0, int(len(pixelGroup) / 2 )):random.randint(int(len(pixelGroup) / 2), len(pixelGroup) - 1)
        ]
    # print(randomPixelRange)
    if frameNumber % random.randint(int(totalFrames / 10), int(totalFrames / 9)) == 0:
        for pixel in randomPixelRange:
            # print(pixel)
            pixels[pixel] = (0,0,0)

def pick_random_color ():
    global COLOR
    COLOR = random.choice(ALL_COLORS)

def grow (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    # print(frameNumber)
    framePercent = frameNumber / totalFrames
    if(frameNumber == 0):
        pick_random_color()
        for pixel in pixelGroup:
            pixels[pixel] = (0,0,0)
    
    
    for pixel in range(len(pixelGroup)):
        if(pixel <= framePercent * len(pixelGroup)):
            pixels[pixelGroup[pixel]] = COLOR

def sin (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    framePercent = frameNumber / totalFrames
    sinWave = math.sin(framePercent * math.pi)
    for pixel in pixelGroup:
        pixels[pixel] = (int(255 * sinWave), 0, 0)

def solid_color (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    for pixel in pixelGroup:
        pixels[pixel] = COLOR

def rainbow_cycle(frameNumber: int, pixelGroup: list[int], totalFrames: int):
    framePercent = frameNumber / totalFrames
    progress = framePercent * 255
    for i in range(len(pixelGroup)):
        rc_index = (i * 256 // len(pixelGroup)) + int(progress)
        pixels[i] = wheel(rc_index & 255)

def calculate_section_number (framePercent: float, sections: int) -> int:
        return math.ceil(framePercent / (1 / sections))

def start_up_animation (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    framePercent = frameNumber / totalFrames
    currentSection = calculate_section_number(framePercent, 5)

    if(currentSection == 1):
        for i in pixelGroup:
            pixels[i] = (0,0,0)
    elif(currentSection == 2):
        for i in pixelGroup:
            pixels[i] = (255,0,0)
        glitch(frameNumber, pixelGroup, totalFrames)
    elif(currentSection == 3):
        rainbow_cycle
        pass
    elif(currentSection == 4):
        pass
    elif(currentSection == 5):
        pass
    
    # Start of animation
    # if frameNumber < totalFrames / animationSections:
    #     # Calculate fade in amount.
    #     fadeAmount = frameNumber * animationSections / totalFrames
    #     # print(fadeAmount)
    #     # Flicker on.
    #     # print(math.sin(framePercent * math.pi))
    #     for pixel in range(len(pixelGroup)):
    #         pixels[pixelGroup[pixel]] = (pixels[pixelGroup[pixel]][0] * int(fadeAmount), pixels[pixelGroup[pixel]][1] * int(fadeAmount), pixels[pixelGroup[pixel]][2] * int(fadeAmount))
    #         # print(pixels[pixelGroup[pixel]])
        
    #     randomPixelRange = pixelGroup[
    #             random.randint(0, int(len(pixelGroup) / 2 )):random.randint(int(len(pixelGroup) / 2), len(pixelGroup))
    #         ]
    #     # print(randomPixelRange)
    #     if frameNumber % random.randint(int(totalFrames / 5), int(totalFrames / 3)) == 0:
    #         for pixel in randomPixelRange:
    #             # print(pixel)
    #             pixels[pixel] = (0,0,0)

    # # End of animation
    # elif frameNumber > (totalFrames / 5) * 4:
    #     for pixel in range(len(pixelGroup)):
    #         pixels[pixelGroup[pixel]] = (255, 0, 0)

    # # Middle of animation
    # else:
    #     # Up the max brightness.
    #     pixels.brightness = 0.5
    #     for pixel in range(len(pixelGroup)):
    #         pixels[pixelGroup[pixel]] = (0, 255, 0)

def heart_beat (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    framePercent = frameNumber / totalFrames
    currentSection = calculate_section_number(framePercent, 12)

    if currentSection == 1:
        for pixel in pixelGroup:
            pixels[pixel] = ((round(RED[0]* 0.5),0,0))
    elif currentSection == 2:
        for pixel in pixelGroup:
            pixels[pixel] = (0,0,0)
    elif currentSection == 3:
        for pixel in pixelGroup:
            pixels[pixel] = ((RED[0],0,0))
    elif currentSection == 4:
        for pixel in pixelGroup:
            pixels[pixel] = (0,0,0)

def random_color (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    if(frameNumber % 30) == 0:
        pixels.fill(random.choice(ALL_COLORS))

def jump (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    def colorRandomPixel ():
        random_index = random.randint(0, len(pixelGroup) - 1)
        random_color = random.choice(ALL_COLORS)
        pixels[pixelGroup[random_index]] = random_color
    for i in range(3):
        colorRandomPixel()

def test (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    for pixel in pixelGroup:
        random_color = random.choice(ALL_COLORS)
        pixels[pixelGroup[pixel]] = random_color

def RunAnimation (animationList: list, framesPerSecond: int = 30, totalFrames: int = 240, times: int = 1):
    for i in range(times):
        for frameNumber in range(totalFrames):
            for animation in animationList:
                animationFunction = animation[0]
                animationPixels = animation[1]
                animationFunction(frameNumber, animationPixels, totalFrames)
            pixels.show()
            time.sleep(1/framesPerSecond)

def RepeatAnimation (animation: function, times: int):
    for i in range(times):
        animation()

def StrandTest ():
    for brightness in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        print("Brightness at "+ str(brightness))
        pixels.fill((0,0,0))
        time.sleep(3)
        pixels.brightness = brightness
        for pixelAmount in range(1, num_pixels):
            print("Testing " + str(pixelAmount) + " pixels")
            testColor = (0,0,0)
            for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,255,255), (255,255,255)]:
                testColor = color
                for pixel in range(pixelAmount):
                    pixels[pixel] = testColor
                pixels.show()
                time.sleep(0.1)

shoulderPixels = [0,1,2,3,4,5]
additionalPixels = [6,7,8,9,10,11]
chestPixels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
baddieShoulderPixels = [19,20,21,22,23,24,25,26,27,28,29,30]
# shoulderPixels = shoulderPixels + additionalPixels
# collarPixels = [6,7,8,9,10,11,12,13,14]
# allPixels = shoulderPixels + collarPixels

while True:
    RunAnimation([
        (grow, shoulderPixels),
        ], 60, 120, 10)
    RunAnimation([
        (random_color, shoulderPixels),
        ], 60, 120, 10)
    RunAnimation([
        (solid_color, shoulderPixels),
        (glitch, shoulderPixels),
        ], 30, 300, 10)
    RunAnimation([
        (rainbow_cycle, shoulderPixels),
        ], 30, 300, 10)
    RunAnimation([
        (heart_beat, shoulderPixels),
        ], 6, 12, 10)
    # RunAnimation(animation2,5)
    # RepeatAnimation(rainbow_cycle, 5)
    # StrandTest()
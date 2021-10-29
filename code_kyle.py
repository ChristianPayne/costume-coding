import time
import board
import neopixel
import math
import random

pixel_pin = board.D24
# num_pixels = 19 + 12
# num_pixels = 38
num_pixels = 124

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.6, auto_write=False, pixel_order=(1, 0, 2))

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

COLOR = GREEN

 
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
    tailLength = 5
    dotColor = WHITE
    tailColor = ORANGE

    framePercent = frameNumber / totalFrames
    for pixel in pixelGroup:
        if(pixel == int(framePercent * len(pixelGroup))):
            pixels[pixelGroup[pixel]] = dotColor

            for i in range(tailLength):
                pixels[pixelGroup[pixel - i - 1]] = tailColor

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

def glitch(frameNumber: int, pixelGroup: list[int], totalFrames: int):
    randomPixelRange = pixelGroup[
            random.randint(0, int(len(pixelGroup) / 2 )):random.randint(int(len(pixelGroup) / 2), len(pixelGroup) - 1)
        ]

    if frameNumber % random.randint(int(totalFrames / 10), int(totalFrames / 9)) == 0:
        for pixel in randomPixelRange:
            # print(pixel)
            pixels[pixel] = (0,0,0)

def grow (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    # print(frameNumber)
    framePercent = frameNumber / totalFrames
    if(frameNumber == 0):
        for pixel in pixelGroup:
            pixels[pixel] = (0,0,0)
    for pixel in range(len(pixelGroup)):
        if(pixel <= framePercent * len(pixelGroup)):
            pixels[pixelGroup[pixel]] = (255, 0, 0)

def color_loop (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    # print(frameNumber)
    framePercent = frameNumber / totalFrames
    for color in ALL_COLORS:
        for pixel in range(len(pixelGroup)):
            if(pixel <= framePercent * len(pixelGroup)):
                pixels[pixelGroup[pixel]] = color
            pixels.show()
        time.sleep(0.1)

def decay (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    framePercentInverse = 1 - (frameNumber / totalFrames)
    if (frameNumber == 0 ):
        ranColor = random.choice(ALL_COLORS)
        for pixel in pixelGroup:
            pixels[pixelGroup[pixel]] = ranColor
    else:
        for pixel in pixelGroup:
            pixels[pixelGroup[pixel]] = (round(pixels[pixelGroup[pixel]][0] * framePercentInverse),round(pixels[pixelGroup[pixel]][1] * framePercentInverse),round(pixels[pixelGroup[pixel]][2] * framePercentInverse))

        

def sin (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    framePercent = frameNumber / totalFrames
    sinWave = math.sin(framePercent * math.pi)
    for pixel in pixelGroup:
        pixels[pixel] = (int(255 * sinWave), 0, 0)

def solid_color (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    for pixel in pixelGroup:
        pixels[pixel] = COLOR

def random_color (frameNumber: int, pixelGroup: list[int], totalFrames: int):
    if(frameNumber % 60) == 0:
        pixels.fill(random.choice(ALL_COLORS))

def rainbow_cycle(frameNumber: int, pixelGroup: list[int], totalFrames: int):
    framePercent = frameNumber / totalFrames
    progress = framePercent * 255
    for i in range(len(pixelGroup)):
        rc_index = (i * 256 // len(pixelGroup)) + int(progress)
        pixels[pixelGroup[i]] = wheel(rc_index & 255)

def calculate_section_number (framePercent: float, sections: int) -> int:
        return math.ceil(framePercent / (1 / sections))


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

def RunAnimation (animationList: list, framesPerSecond: int = 30, totalFrames: int = 240, times: int = 1, args: dict = {}):
    for i in range(times):
        for frameNumber in range(totalFrames):
            pixels.fill((0,0,0))
            for animation in animationList:
                animationFunction = animation[0]
                animationPixels = animation[1]
                animationFunction(frameNumber,animationPixels,totalFrames)
            pixels.show()
            time.sleep(1/framesPerSecond)

def RepeatAnimation (animation: function, times: int):
    for i in range(times):
        animation()

def StrandTest ():
    for brightness in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
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
                time.sleep(0.025)

left_chest = list(range(0, 37))
left_shoulder = list(range(38, 43))
back = list(range(44, 81))
right_shoulder = list(range(82, 87))
right_chest = list(range(88, 123))

all_pixels = range(0,num_pixels)

# print(right_chest)


while True:
    
    # StrandTest()


    # Finished animations
    # -----------------------
    # RunAnimation([
    #     (heart_beat, shoulderPixels),
    #     ], 6, 12, 2)

    # RunAnimation([
    #     (sin, all_pixels),
    #     ], 30, 10, 5)

    # RunAnimation([
    #     (heart_beat, right_chest + left_chest),
    #     ], 30, 60, 1)
    
    # RunAnimation([
    #     (grow, all_pixels),
    #     ], 180, 90, 5)
    # pixels.fill((0,0,0))
    # pixels.show()
    # time.sleep(1)
    
    RunAnimation([
        (decay, all_pixels),
        ], 20, 30, 5)
    pixels.fill((0,0,0))
    pixels.show() 
    time.sleep(1)
    # Needs to be refined,,,
    # RunAnimation([
    #     (color_loop, all_pixels),
    #     ], 20, 30, 5)
    # pixels.fill((0,0,0))
    # pixels.show()
    # time.sleep(1)
    # RunAnimation([
    #     (test, all_pixels),
    #     ], 20, 30, 5)
    # pixels.fill((0,0,0))
    # pixels.show()
    # time.sleep(1)
    # RunAnimation([
    #     (jump, all_pixels),
    #     ], 20, 30, 5)
    # pixels.fill((0,0,0))
    # pixels.show()
    # time.sleep(1)
    # RunAnimation([
    #     (jump, all_pixels),
    #     ], 10, 30, 5)
    # pixels.fill((0,0,0))
    # pixels.show()
    # time.sleep(1)
    # RunAnimation([
    #     (rainbow_cycle, left_chest),
    #     (rainbow_cycle, right_chest),
    #     (rainbow_cycle, left_shoulder + right_shoulder),
    #     (rainbow_cycle, back),
    #     ], 180, 90, 5)
    # pixels.fill((0,0,0))
    # pixels.show()
    # time.sleep(1)
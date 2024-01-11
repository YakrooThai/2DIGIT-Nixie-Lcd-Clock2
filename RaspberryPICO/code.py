import micropython
import board, busio, displayio, time
import adafruit_displayio_ssd1306
import adafruit_imageload

import digitalio
from time import sleep
from adafruit_st7789 import ST7789

import neopixel
import adafruit_ds3231
import gifio
import os, sys
import gc

import machine

import terminalio
from adafruit_display_text import label

from adafruit_bitmap_font import bitmap_font
import microcontroller

Buzz = digitalio.DigitalInOut(board.GP26)
Buzz.direction = digitalio.Direction.OUTPUT
Buzz.value = False
#----ST7735
cs1 = digitalio.DigitalInOut(board.GP2)
cs1.direction = digitalio.Direction.OUTPUT
cs2 = digitalio.DigitalInOut(board.GP7)
cs2.direction = digitalio.Direction.OUTPUT
cs1.value = True
cs2.value = True

#----ds3231
SDA = board.GP20
SCL = board.GP21
i2c = busio.I2C(SCL, SDA)
rtc = adafruit_ds3231.DS3231(i2c)
days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
month = (" ","Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec")
        
#----WS2812B
# Update this to match the number of NeoPixel LEDs connected to your board.
fbright=0.14 
num_pixels = 3 
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = fbright

GreenB = 0x00CC00

BLACK = (0, 0, 0) 
RR = (250, 0, 0)  # color to blink
GG = (0, 250, 0)
BB = (0, 0, 250)
WHITE = (255, 255, 255)

pixels[0] = WHITE
pixels[1] = WHITE
pixels[2] = WHITE


pixels.show()
#===================================================================
tft_cs1 = board.GP1
tft_cs2 = board.GP3
tft_dc = board.GP16
tft_dc2 = board.GP6
tft_res = board.GP17

spi_mosi = board.GP11 
spi_clk  = board.GP10 

displayio.release_displays()
spi = busio.SPI(spi_clk, MOSI=spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs1, reset=tft_res,baudrate=3200000)
display = ST7789(display_bus, rotation=180, width=240, height=320)

Nixie_Yakroo = displayio.OnDiskBitmap("/Yakroo108.bmp")
Nixie_H = displayio.OnDiskBitmap("/hour.bmp")
Nixie_M = displayio.OnDiskBitmap("/min.bmp")
wait_c = displayio.OnDiskBitmap("/waitC.bmp")


def digit(n):
    if 0 <= n <= 9:
        return displayio.TileGrid(Nixie_bitmaps[n], pixel_shader=Nixie_bitmaps[n].pixel_shader)

group = displayio.Group()
tile_grid = displayio.TileGrid(Nixie_Yakroo, pixel_shader=Nixie_Yakroo.pixel_shader,x=60, y=80)
group.append(tile_grid)
display.show(group)

sleep(.1)
cs2.value = True
cs1.value = False

Nixie_bitmaps = [
                        displayio.OnDiskBitmap("/0/b00.bmp"),
                        displayio.OnDiskBitmap("/0/b01.bmp"),
                        displayio.OnDiskBitmap("/0/b02.bmp"),
                        displayio.OnDiskBitmap("/0/b03.bmp"),
                        displayio.OnDiskBitmap("/0/b04.bmp"),
                        displayio.OnDiskBitmap("/0/b05.bmp"),
                        displayio.OnDiskBitmap("/0/b06.bmp"),
                        displayio.OnDiskBitmap("/0/b07.bmp"),
                        displayio.OnDiskBitmap("/0/b08.bmp"),
                        displayio.OnDiskBitmap("/0/b09.bmp")
                    ]

def clear_2Digit():
    cs1.value = True
    cs2.value = True
    tile_grid = displayio.TileGrid(wait_c, pixel_shader=Nixie_Yakroo.pixel_shader,x=60, y=80)
    group.append(tile_grid)
    display.refresh()   
    sleep(.01)
    cs1.value = False
    cs2.value = False
    group.remove(tile_grid)   

def clear_Hour():
    cs1.value = True
    cs2.value = True
    tile_grid = displayio.TileGrid(Nixie_H, pixel_shader=Nixie_Yakroo.pixel_shader,x=60, y=80)
    group.append(tile_grid)
    display.refresh()   
    sleep(.01)
    cs1.value = False
    cs2.value = False
    group.remove(tile_grid)
    
def clear_Min():
    cs1.value = True
    cs2.value = True
    tile_grid = displayio.TileGrid(Nixie_M, pixel_shader=Nixie_Yakroo.pixel_shader,x=60, y=80)
    group.append(tile_grid)
    display.refresh()   
    sleep(.01)
    cs1.value = False
    cs2.value = False
    group.remove(tile_grid)     
def countsecDG1(n):
    global group  # Declare 'group' as global
    cs1.value = True
    cs2.value = False

    num = digit(n)
    if num:
        tile_grid = num
        tile_grid.x = 60
        tile_grid.y = 50
        group.append(tile_grid)
        display.refresh()
        sleep(.01)
        cs1.value = False
        group.remove(tile_grid)       
def countsecDG2(n):
    global group  # Declare 'group' as global

    cs1.value = False
    cs2.value = True
     
    num = digit(n)
    if num:
        tile_grid = num
        tile_grid.x = 60
        tile_grid.y = 50
        group.append(tile_grid)
        display.refresh()
        sleep(.01)
        cs2.value = False
        group.remove(tile_grid)
        
def WsR():
    pixels[0] = RR
    pixels[1] = RR

    
def WsG():
    pixels[0] = GG
    pixels[1] = GG
    

def WsB():
    pixels[0] = BB
    pixels[1] = BB
      
def WsW():
    pixels[0] = WHITE
    pixels[1] = WHITE        
        
sleep(1)
num1=0
num2=0
cntled=0

NumSec=0
tmpDec=0
countsecDG1(0)
countsecDG2(0)
NumSec=0

Buzz.value = True
time.sleep(0.08)
Buzz.value = False
time.sleep(0.2)
Buzz.value = True
time.sleep(0.08)
Buzz.value = False 
#@RTC=,2023,9,2,Wednesday,22,23,32,2,#
    #                 year, mon, date, hour, min, sec, wday, yday, isdst
#t = time.struct_time((2024, 1 , 10  ,20  , 57 , 24 , 2   , -1  , -1))
#print("Setting time to:", t)  
#rtc.datetime = t
while True:
    t = rtc.datetime
   
        #if DEBUG:
    print("The date is {} {}/{}/{}".format(
                days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
               )
    )
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))

    NumSec=int(t.tm_hour)    
    num1 = int(NumSec / 10)
    num2 = NumSec % 10
    clear_Hour()
    sleep(.6)
    countsecDG1(num1)
    countsecDG2(num2)    
    sleep(2)
    
    clear_Min()
    sleep(.6)
    NumSec=int(t.tm_min)    
    num1 = int(NumSec / 10)
    num2 = NumSec % 10    
    countsecDG1(num1)
    countsecDG2(num2)
    sleep(3)
    
    clear_2Digit()
    sleep(3)
    sleep(3)
    sleep(1)
    sleep(1)




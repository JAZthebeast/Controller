import RPi.GPIO as GPIO
import PCF8591 as ADC
import pygame as pg
import math

pins = { 
		'A': 11,
		'B': 12,
		'C': 13,
		'D': 15,
		}

def setup():   
	ADC.setup(0x48)	
	GPIO.setmode(GPIO.BOARD)
	for pin in pins:
		GPIO.setup(pins[pin], GPIO.IN)

def sqaure_to_circle():
	x = -128 + ADC.read(0)
	y = -128 + ADC.read(1)
	u, v = abs(x), abs(y)
	if u < v:
		u, v = v, u
	d = 1/math.cos(math.atan2(v, u))
	return int(x/d), int(y/d)
def input_values(pins, pressed):
	x, y = sqaure_to_circle()
	for pin in pins:
		if GPIO.input(pins[pin]) == 1:
			if pin in pressed:
				pressed.remove(pin)
		elif GPIO.input(pins[pin]) == 0:
			if not pin in pressed:
				pressed.append(pin)
	return x, y, pressed

def circle_outline(x, y, display, pressed, letter):
	pg.draw.circle(display, (0, 0, 0,), (x, y), 50)
	if letter in pressed:
		colour = (0, 0, 0)
	else:
		colour = (255, 255, 255)
	pg.draw.circle(display, (colour), (x, y), 40)
def loop(pins):
	pressed = []
	display = pg.display.set_mode((1000, 500))
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				destroy()
		x, y, pressed = input_values(pins, pressed)
		pg.draw.circle(display, (0, 0, 0), (250 + x, 250 - y), 100)
		circle_outline(750, 150, display, pressed, 'A')
		circle_outline(850, 250, display, pressed, 'B')
		circle_outline(750, 350, display, pressed, 'C')
		circle_outline(650, 250, display, pressed, 'D')
		pg.display.update()
		display.fill((255, 255, 255))

def destroy():
	GPIO.cleanup()
	pg.display.quit()
	pg.quit()

setup()
try:
    loop(pins)
except KeyboardInterrupt: 
	destroy()

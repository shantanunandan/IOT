from django.shortcuts import render
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default() 
sensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BCM)
led_pin = 20
temp_pin = 21
GPIO.setup(led_pin,GPIO.OUT)

def index(request):
	hum,temperature = Adafruit_DHT.read_retry(sensor,temp_pin)
	value = str(temperature)
	return render(request,"home.html",{"temp":value})

def led(request):
	if request.method=="POST":
		hum,temperature = Adafruit_DHT.read_retry(sensor,temp_pin)
		value = request.POST.get('led_status')
		if(value=="on"):
			GPIO.output(led_pin,GPIO.HIGH)
		elif(value=="off"):
			GPIO.output(led_pin,GPIO.LOW)
		return render(request,"home.html",{"temp":temperature})
	else:
		return render(request,"home.html")

def oled(request):
	if request.method=="POST":
		hum,temperature = Adafruit_DHT.read_retry(sensor,temp_pin)
		value = str(temperature)
		disp.clear()
		value = request.POST.get("oled")
		draw.text((x, top),str(value), font=font, fill=255)
		disp.image(image)
		disp.display()
		time.sleep(.1)
		return render(request,"home.html",{"temp":temperature})
	else:
		return render(request,"home.html") 

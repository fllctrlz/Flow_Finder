import epd2in7
import Image
import ImageFont
import ImageDraw
import requests
import json
import time


def displayText(text):
    epd = epd2in7.EPD()
    epd.init()

    #Trent Test
    #image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)    # 255: clear the image with white
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 18)
    draw.text((20, 100), text, font = font, fill = 0)

    #Trent Test
    #epd.display_frame(epd.get_frame_buffer(image))
    epd.display_frame(epd.get_frame_buffer(image.rotate(90, expand=True)))

def main(data):
    epd = epd2in7.EPD()
    epd.init()

    #Trent Test
    #image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 24)

    total = 0
    for d in data:
	 total += d["totalLitres"]
    total = float(total)

    
   
    i = 0
    for d in data:
        k = float(d["totalLitres"])/total
    
	
	draw.rectangle((125, 28*i, 125+125*k, 28*i+20), fill=0)	
	draw.text((20, 0+28*i), d["name"] , font = font, fill = 0)
	draw.text((210, 0+28*i),str(d["totalLitres"]) + " L", font = font, fill = 0)
	i = i+1


    #Trent Test
    #epd.display_frame(epd.get_frame_buffer(image))
    epd.display_frame(epd.get_frame_buffer(image.rotate(90, expand=True)))
    
def oneUpdate():
	with open("/home/pi/Desktop/Flow_Finder/ip.txt", "r") as file:
		output = file.read()
	displayText(output)
	time.sleep(40)
	while(True):
		data = requests.get('http://localhost:3000/magnet/total').json()
    		main(data)
		time.sleep(20)
		

	

if __name__ == '__main__':
   
    oneUpdate()


		    #draw.rectangle((0, 76, 176, 96), fill = 0)
		    #draw.text((18, 80), 'Hello world!', font = font, fill = 0)
		    #draw.line((10, 130, 10, 180), fill = 0)
		    #draw.line((10, 130, 50, 130), fill = 0)
		    #draw.line((50, 130, 50, 180), fill = 0)
		    #draw.line((10, 180, 50, 180), fill = 0)
		    #draw.line((10, 130, 50, 180), fill = 0)
		    #draw.line((50, 130, 10, 180), fill = 0)
		    #draw.arc((90, 190, 150, 250), 0, 360, fill = 0)
		    #draw.chord((90, 120, 150, 180), 0, 360, fill = 0)
		    #draw.rectangle((10, 200, 50, 250), fill = 0)

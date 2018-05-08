'''
Author: CTRL-Z Robotics

This program will take information from the server and display it onto the E-Ink display.
'''


#Importing various libraries 
import epd2in7
import Image
import ImageFont
import ImageDraw
import requests
import json
import time



#this function will set the variables that will be used when we call it later.
#we call it when we want to display the Wi-Fi Ip Adress, so we can use it to access the server
def displayText(text):
    epd = epd2in7.EPD()
    epd.init()

    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 18)
    draw.text((20, 100), text, font = font, fill = 0)

    epd.display_frame(epd.get_frame_buffer(image.rotate(90, expand=True)))


#this method will display each person's water consumption and the bar graph
def main(data):
    epd = epd2in7.EPD()
    epd.init()

    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 24)
	#finding total water used among all users
    total = 0
    for d in data:
	 total += d["totalLitres"]
    total = float(total)

   #finding each persons percentage of total water usage
    i = 0
    for d in data:
        k = float(d["totalLitres"])/total
	#displaying the bars for each person by extending it proportionally to their percentage
	draw.rectangle((103, 28*i, 103+125*k, 28*i+20), fill=0)	
	#displaying each persons name
	draw.text((2, 28*i), d["name"] , font = font, fill = 0)
	#display each persons water consumption
	draw.text((175, 28*i),str(round(d["totalLitres"]/3.85,1)) + " Gal", font = font, fill = 0)

	i = i+1

    epd.display_frame(epd.get_frame_buffer(image.rotate(90, expand=True)))
    

#main method that calls the other methods
#it also gets the information from the server
def oneUpdate():
	with open("/home/pi/Desktop/Flow_Finder/ip.txt", "r") as file:
		output = file.read()
	displayText(output)
	#time.sleep(40)
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

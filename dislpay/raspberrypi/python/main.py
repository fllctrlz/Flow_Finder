import epd2in7
import Image
import ImageFont
import ImageDraw
import requests
import json

def main(data):
    epd = epd2in7.EPD()
    epd.init()

    image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 18)
    i = 1
    for d in data:
	draw.text((20, 20*i), d["name"] +": "+ str(d["totalLitres"]), font = font, fill = 0)
	i = i+1
    epd.display_frame(epd.get_frame_buffer(image))


if __name__ == '__main__':
    data = requests.get('http://localhost:3000/magnet/total').json()
    main(data)

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

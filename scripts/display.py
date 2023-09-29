import sys
import time
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306
import socket
import os

class Display:
    def __init__(self):
        self.width = 128
        self.height = 64
        self.font = ImageFont.load_default()
        self.enabled = True  # Initialize as True, will be set to False on error
        self.ip = self.get_ip_address()

        try:
            self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)
            self.disp.begin()
            self.disp.clear()
            self.disp.display()
        except RuntimeError as e:
            print(f'Display: {e}', file=sys.stderr)
            self.enabled = False

    def display_time(self):
        if not self.enabled:
            return

        image = Image.new('1', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        
        # Clear the image buffer
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Get the current time
        current_time = time.strftime('%H:%M:%S')
        
        # Draw the time on the image
        draw.text((0, 1), current_time, font=self.font, fill=255)

        # Display the image
        self.disp.image(image)
        self.disp.display()

    def display_msg(self, status, img_count):
        if not self.enabled:
            return

        msg = [f'{status}', 
                time.strftime('%H:%M:%S'),
                f'Img count: {img_count}',
                f'IP: {self.ip}']

        
        image = Image.new('1', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        
        # Clear the image buffer
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        #_, font_height = self.font.getsize('Sample Text')
        x, y = 0, 0
        for item in msg:
            draw.text((x, y), item, font=self.font, fill=255)
            y += 14
        

        # Display the image
        self.disp.image(image)
        self.disp.display()    

    def clear_display(self):
        if not self.enabled:
            return
        image = Image.new('1', (self.width, self.height))
        self.disp.image(image)
        self.disp.display()


    def get_ip_address(self):
        try:
            hostname = socket.gethostname()
            result = os.popen(f"ifconfig eth0").read()
            IPAddr = result.split("inet ")[1].split()[0]
            return f'{hostname}@{IPAddr}'
        except:
            return "Unknown"


if __name__ == '__main__':
    disp = Display()
    ip = disp.get_ip_address()
    

    try:
        while True:
            msg = [f'Imaging status', 
                   time.strftime('%H:%M:%S'),
                   f'IP: {ip}']
            disp.display_msg(msg)
            current_second_fraction = time.time() % 1
            sleep_duration = 1 - current_second_fraction
            time.sleep(sleep_duration)
    except KeyboardInterrupt:
        disp.clear_display()

    finally:
        disp.clear_display()
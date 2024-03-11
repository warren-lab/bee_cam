import adafruit_ds3231
import time
import board
import datetime
## https://docs.circuitpython.org/projects/ds3231/en/latest/
print(datetime.datetime.now())
# i2c = board.I2C()  # uses board.SCL and board.SDA
# rtc = adafruit_ds3231.DS3231(i2c)


# # For setting the time... system time to rtc...
# rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))

# # 
# t = rtc.datetime
# print(t)
# print(t.tm_hour, t.tm_min)


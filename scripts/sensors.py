from datetime import datetime
import os
import time
## temperature data...
import board
import adafruit_si7021
## light sensor data
import board
import adafruit_tsl2591
from csv import DictWriter


"""
Goal is to make a main sensor class and then 2 child classes for the individual sensors

- So these sensors will have all of the 
"""

# Initialized some exceptions that will be utilized as well
class DarkPeriod(Exception):
    """Raised when the Lux value for 5 concurrent samples is below the threshold"""
    pass 


class Sensor:
    # dictionary of sensor data intrinsict for each sensor type
    data_dict ={} 
    # Initialized the time domain for this dictionary
    data_dict['time'] = []
    # Initialized the image file key for this dictionary
    data_dict['image_filename'] = []

    # Create library object using our Bus I2C port
    i2c = board.I2C()  # uses board.SCL and board.SDA
    def __init__(self, device = None):

        ## name of sensor
        self.sensor_device = device

    def get_data(self,sensor_type):
        """
        Depending on the child class sensor device get_data will be
        used in order to grab the current sensor reading from the sensor.
        """
        data = getattr(self.sensor_device,sensor_type) # object, attribute
        return data
    def add_data(self,sensor_type):
        """
        Add data into the dictionary under the key of the sensor type

        Also returns the current data that was recieved in case that wants to be examined
        """
        data = self.get_data(sensor_type)
        ## check to see if the key exists first and if it does then add to it
        if sensor_type not in self.data_dict.keys():
            self.data_dict[sensor_type] = [data]
        ## if key doesn't exist then create
        else:
            self.data_dict[sensor_type].append(data)
            
        return data
    def display(self):
        """
        Display the sensor dictionary
        """
        print("Sensor Data")
        d = self.data_dict
        print(d)
    def reset_dict(self):
        """
        reset the dictionary
        """
        return

    # def write_csv(self):
    #     """
    #     Write the saved sensor data to file

    #     This can be used in the case where you want specific information fo
    #     """


# Temperature and Relative Humidity Sensor 
class TempRHSensor(Sensor):
    def __init__(self):
        super().__init__(adafruit_si7021.SI7021(self.i2c))

        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
        ## sensor types:
        self.sensor_types = ['temperature','relative_humidity']
    def temp_rh_data(self):
        """
        gets the temperature and adds it to the dictionary but also 
        returns the temperature 
        """
        ## adds data to the dictionary
        ### also provides current data point
        data1 = self.add_data(self.sensor_types[0])
        data2 = self.add_data(self.sensor_types[1])
        ## update the dictionary

        return data1,data2
#  Light Sensor
class LightSensor(Sensor):
    """
    Need to enable error handling so that if the sensor is not connecting we can continue
    with the remaining sensors and the imaging...
    """
    def __init__(self):
        super().__init__(adafruit_tsl2591.TSL2591(self.i2c))
        #self.number_of_reads = config['Light'].getint('number_of_reads')
        #self.read_dt = config['Light'].getfloat('read_dt')
        self.sensor_device.gain = adafruit_tsl2591.GAIN_MED
        self.sensor_device.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS
        self.sensor_types = ['lux','visible','infrared','full_spectrum']

        # set the light sensor lux threshold (https://www.engineeringtoolbox.com/light-level-rooms-d_708.html)
        self._lux_thr = 10
        self.counter = 0 # interal counter for this sensor for how many readings are below threshold (max 5)
    
    def light_data(self):
        """
        gets the temperature and adds it to the dictionary but also 
        returns the temperature 
        """
        # get light data
        lux,viz,ir,full = self.sensor_types

        # prior to adding the data to the dictionary need to verify that the lux in in range


        ## adds data to the dictionary
        ### also provides current data point
        data1 = self.add_data(self.sensor_types[0])
        data2 = self.add_data(self.sensor_types[1])
        data3 = self.add_data(self.sensor_types[2])
        data4 = self.add_data(self.sensor_types[3])
        ## update the dictionary
        return data1,data2,data3, data4
    def get_lux(self):
        """
        
        check to see if the lux over several measurements is under the threshold
        if the lux is under the threshold for 5 measurements (maybe have it be more or less?)
        then will send signal to kill data collection process
        """

        return self.get_data(self.sensor_types[0])
    
# class Battery(Sensor):
#     """
#     Sensor class specific to the Adafruit MAX17048 Lipo Battery Fuel Gauge

#     Current Issues:
#      - Current Charge Estimate
#      - Issue with calibration of the battery  

#     """
class GPS(Sensor):
    """
    Sensor class specific to the Adafruit Mini GPS PA1010D Module

    Current Issues:
     - Need to essentially enable the write of the RTC time from the GPS to the Pi System Time
     - Afterwar

    """
class RTC(Sensor):
    """
    Sensor class specific to the Adafruit DS3231 Precision RTC - STEMMA QT

    This sensor will act as a back up RTC as the supercapacitor on the WittyPi 4 Mini will not 
    maintain time while powered off for a long period. So, during transit of the sensor system this
    RTC will be utilized in place of the WittyPi which will be disconnected from the power supply.

    Upon set up of the sensor system in the field this sensor is the first one that should be used ensuring
    the time on the device is calibrated.

    https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time
    - we needed to use this tutorial in order to get rid of the fake-hwclock functionality that the Raspberry Pi
    has built in when ther eis no RTC... What this means is that we are then going to essentially override this 
    and implement the DS3231 sensor in its place as a reliable RTC...

        - NOTE -> Witty Pi also has RTC... so will need to detemine conflicts with that... and ensure that the wittyPi
        gets calibrated by the system. 
        - NOTE -> Witty Pi essentially needs to be same time as RTC/System because it will act as power managment and 
        ensure the start up and shutdown times...

    After setting the DS3231 to be the RTC for the Pi then we needed to anable the network time protocol
    synchronization
        - enable NTP sync
        ```sudo timedatectl set-ntp true```
        
        - update system time
        ```sudo systemctl restart systemd-timesyncd```

        - finally check the current date
        ```date```
    
    After performing all of these steps this sensor will not be integrated into 
    the Sensor stack in the control script as it is already running in the background
    """

class WittyPi(Sensor):
    """
    Sensor class specific to the UUGear WittyPi 4 Mini

    Current Issues:
        -  The current issue is that we are unable to get the correct RTC time on the pi when we want to sync
        - The solution for this is to instead utilize the GPS RTC first to write to the system time and then write the sytstem time to the WittyPi. That way we have complete accuracy...
            - we could use the other RTC but the wittypi has more robust functionality for startup and shutdown based on the datetime and ensuring the time accuracy is important
        - Do some troubleshooting in order to check the differences in the system, RTC from GPS and the wittypi RTC

    Upon initalizing this sensor when the board is booted the GPS Sensor RTC will be written to the WittyPi. This should be done by using a BashScript...
    
    """





class MultiSensor(Sensor):
    """
    Class that holds the various different sensors for acquiring data

    This will reduce the amount of complexity in the control script.

    It also allows for the saving of all sensor data to csv

    
    NEED TO DETERMINE:
    - periodic batching for backup of CSV
    - do backup everytime we get sensor data
    - or do a combo of both methods
    
    NEED TO ADD:
    - need more error handling
    - need to integrate time component..
    - need to also have realtime monitoring...


    """
    def __init__(self,path_sensors):
        """
        Initialize the different sensor classes
        """
        super().__init__()
        self.__temp_rh = TempRHSensor()
        self.__light = LightSensor()
        # self.__battery = 
        # Generate a filename based on the current timestamp and store it as a class property
        ### This could be placed in a different place...
        start_time= datetime.now().strftime('%Y%m%d_%H%M%S')
        self.filename = f'{path_sensors}/sensor_data_{start_time}.csv'# all data is written to this CSV...

    def add_data(self,img_file,date_time):
        """
        Similar to the prior classes this method will
        focus on adding the data to the sensor data dictionary

        However, this method essentially just calls all of the sensor 
        data acquisition methods.
        """
        ## Add the image and time to the dictionary
        #print(date_time)
        self.data_dict['time'].append(date_time)
        self.data_dict["image_filename"].append(img_file)
        ## Add Temperature and Humidity
        d_t, d_rh = self.__temp_rh.temp_rh_data()
        ## Add Light Data
        d_lux, d_v, d_ir, d_fs= self.__light.light_data()
        
        ## Get the cuurrent data
        #print("Current Data")
        #self.display() # displays all data using the sensor display method
        #return d_t, d_rh, d_lux, d_v, d_ir, d_fs
    
    def append_to_csv(self):
        """
        Create and or append the sensor data to the csv file

        ADD into the CSVfile the image name as well which is going to require a function input...
        """
        if not os.path.exists(self.filename):
            # create the csv with headers..
            with open(self.filename, 'w') as data_file:
                    csv_writer = DictWriter(data_file, fieldnames =self.data_dict.keys())
                    csv_writer.writeheader() # write the header...
        with open(self.filename, 'a') as data_file:
            try:
                # Try to pass the dictionary into the csv 
                csv_writer = DictWriter(data_file, fieldnames =self.data_dict.keys())
                #print(self.data_dict.values())
                # first got the length of the list...
                len_list = len(list(self.data_dict.values())[0])
                # looping over each time instance:
                for t in range(len_list):
                    row_data = {}
                    for k in self.data_dict.keys():
                        # add data at this time for sensor 'k' to dictionary
                        row_data[k] = self.data_dict[k][t]
                    # write this row...of data for the timestep...
                    # before the next time instance write what we have to csv
                    csv_writer.writerow(row_data) # appends data to the headers
                
                # reset the data_dict
                for k in self.data_dict:
                    self.data_dict[k] = []
                print("CLEAR!")
                print(self.data_dict)
                #print(self.data_dict)
            ## FIGURE OUT MORE ON RAISING EXCEPTIONS AND STUFF...
            except Exception as e:
                print(f"An error occurred while appending to the CSV file: {e}")

if __name__ == "__main__":
    """
    Testing Procedure for temperature sensor
    """
    print("Working")
    
    sensors = MultiSensor(path_sensors="/home/pi/data/")
    # Start timer
    start_time = time.time()

    try:
        curr_time = start_time
        while True:
            print("In Loop")
            time.sleep(2)
            time_current_split = datetime.now().strftime('%Y%m%d%H%M%S')
            name = 'bob'
            img_name = str(name + '_' + time_current_split + '.jpg')
            sensors.add_data(img_name,time_current_split )
            if (time.time()-curr_time) >= 30:
                curr_time = time.time()
                sensors.append_to_csv()
            
    except KeyboardInterrupt:
        print("Exiting")
        sensors.display()

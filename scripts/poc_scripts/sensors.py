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

class Sensor:
    # dictionary of sensor data intrinsict for each sensor type
    data_dict ={} 

    # Create library object using our Bus I2C port
    i2c = board.I2C()  # uses board.SCL and board.SDA
    def __init__(self):

        ## name of sensor
        self.sensor_device = None

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
        super().__init__()

        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
        self.sensor_device = adafruit_si7021.SI7021(self.i2c)
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
        super().__init__()
        #self.number_of_reads = config['Light'].getint('number_of_reads')
        #self.read_dt = config['Light'].getfloat('read_dt')
        self.sensor_device = adafruit_tsl2591.TSL2591(self.i2c)
        self.sensor_device.gain = adafruit_tsl2591.GAIN_MED
        self.sensor_device.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS
        self.sensor_types = ['lux','visible','infrared','full_spectrum']
    def light_data(self):
        """
        gets the temperature and adds it to the dictionary but also 
        returns the temperature 
        """
        ## adds data to the dictionary
        ### also provides current data point
        data1 = self.add_data(self.sensor_types[0])
        data2 = self.add_data(self.sensor_types[1])
        data3 = self.add_data(self.sensor_types[2])
        data4 = self.add_data(self.sensor_types[3])
        ## update the dictionary

        return data1,data2,data3, data4



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
    def __init__(self):
        """
        Initialize the different sensor classes
        """
        super().__init__()
        self.__temp_rh = TempRHSensor()
        self.__light = LightSensor()
        # Generate a filename based on the current timestamp and store it as a class property
        ### This could be placed in a different place...
        start_time= datetime.now().strftime('%Y%m%d')
        self.filename = f'sensor_data_{start_time}.csv'# all data is written to this CSV...
        # Create the CSV initially here...
        with open(self.filename, 'w') as new_csv:
            pass
        
    def add_data(self):
        """
        Similar to the prior classes this method will
        focus on adding the data to the sensor data dictionary

        However, this method essentially just calls all of the sensor 
        data acquisition methods.
        """
        d_t, d_rh = self.__temp_rh.temp_rh_data()
        d_lux, d_v, d_ir, d_fs= self.__light.light_data()
        print("Current Data")
        self.__temp_rh.display()
        #return d_t, d_rh, d_lux, d_v, d_ir, d_fs
    
    def append_to_csv(self):
        """
        Create and or append the sensor data to the csv file


        CONTINUE TO WORK ON THIS -> FIX STRUCTURE AND DICT RESET FOR ALL SENSOR
        """
        with open(self.filename, 'w') as data_file:
            try:
                # Try to pass the dictionary into the csv 
                csv_writer = DictWriter(data_file, fieldnames =self.data_dict.keys())
                csv_writer.writerow(self.data_dict)
                self.data_dict = {} # reset the data_dict...
                print(self.data_dict)
            ## FIGURE OUT MORE ON RAISING EXCEPTIONS AND STUFF...
            except Exception as e:
                print(f"An error occurred while appending to the CSV file: {e}")









#     def __init__(self):
#         # Initialize an empty dictionary to store sensor data
#         self.data_dict = {}
        
#         # Generate a filename based on the current timestamp and store it as a class property
#         timestamp = datetime.now().strftime('%Y%m%d')
#         self.filename = f'sensor_data_{timestamp}.csv'


#     def get_data(self, key, value):
#         """Store data in the dictionary."""
#         self.data_dict[key] = value
    
#     def get_dict(self, new_dict):
#         """Combine an external dictionary with the existing data_dict."""
#         self.data_dict.update(new_dict)

#     def create_csv(self):
#         if not os.path.exists(self.filename):
#             with open(self.filename, 'w', newline='') as f:
#                 writer = csv.DictWriter(f, fieldnames=self.data_dict.keys())
#                 writer.writeheader()

#     def append_to_csv(self):
#         """Append the current data to the existing CSV file."""
#         try:
#             with open(self.filename, 'a', newline='') as f:
#                 writer = csv.DictWriter(f, fieldnames=self.data_dict.keys())
#                 writer.writerow(self.data_dict)
#             self.data_dict = {}
#         except Exception as e:
#             print(f"An error occurred while appending to the CSV file: {e}")

if __name__ == "__main__":
    """
    Testing Procedure for temperature sensor
    """
    print("Working")
    
    sensors = MultiSensor()
    # Start timer
    start_time = time.time()

    try:
        curr_time = start_time
        while True:
            print("In Loop")
            time.sleep(2)
            sensors.add_data()
            if (time.time()-curr_time) >= 30:
                print("yo")
                curr_time = time.time()
                sensors.append_to_csv()


    except KeyboardInterrupt:
        print("Exiting")
        sensors.display()

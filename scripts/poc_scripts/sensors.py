import csv
from datetime import datetime
import os
import time
## temperature data...
import board
import adafruit_si7021
## light sensor data
import board
import adafruit_tsl2591


"""
Goal is to make a main sensor class and then 2 child classes for the individual sensors

- So these sensors will have all of the 
"""

class sensors:
    # dictionary of sensor data intrinsict for each sensor type
    data_dict ={} 
    def __init__(self):

        ## name of sensor
        self.sensor_device = 'sensor'

        # Generate a filename based on the current timestamp and store it as a class property
        timestamp = datetime.now().strftime('%Y%m%d')
        self.filename = f'sensor_data_{timestamp}.csv' # all data is written to this CSV...
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
    #def write_csv(self,)


# Temperature and Relative Humidity Sensor 
class temp_rh(sensors):
    def __init__(self):
        super().__init__()
        # Create library object using our Bus I2C port
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
        self.sensor_device = adafruit_si7021.SI7021(i2c)
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
    
    def display(self):
        d = self.data_dict
        print(d)

#  Light Sensor
class lightsensor(sensors):
    def __init__(self):
        super().__init__()
        #self.number_of_reads = config['Light'].getint('number_of_reads')
        #self.read_dt = config['Light'].getfloat('read_dt')
        self.device = adafruit_tsl2591.TSL2591(board.I2C())
        self.device.gain = adafruit_tsl2591.GAIN_MED
        self.device.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS
        self.sensor_types = ['lux','visible','infrared','full_spectrum']
    def temp_rh_data(self):
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

        return data1,data2
    
    def display(self):
        d = self.data_dict
        print(d)



# class multisensors:
#     def __init__(self):

    



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
    temp_sensor = temp_rh()

    try:
        while True:
            print("In Loop")
            time.sleep(2)
            data = temp_sensor.temp_rh_data()
            print(data)

    except KeyboardInterrupt:
        print("Exiting")
        temp_sensor.display()

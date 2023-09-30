import csv
from datetime import datetime
import os

"""
Goal is to make a main sensor class and then 2 child classes for the individual sensors

- So these sensors will have all of the 
"""

class SensorData:
    def __init__(self):
        # Initialize an empty dictionary to store sensor data
        self.data_dict = {}
        
        # Generate a filename based on the current timestamp and store it as a class property
        timestamp = datetime.now().strftime('%Y%m%d')
        self.filename = f'sensor_data_{timestamp}.csv'


    def get_data(self, key, value):
        """Store data in the dictionary."""
        self.data_dict[key] = value
    
    def get_dict(self, new_dict):
        """Combine an external dictionary with the existing data_dict."""
        self.data_dict.update(new_dict)

    def create_csv(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.data_dict.keys())
                writer.writeheader()

    def append_to_csv(self):
        """Append the current data to the existing CSV file."""
        try:
            with open(self.filename, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.data_dict.keys())
                writer.writerow(self.data_dict)
            self.data_dict = {}
        except Exception as e:
            print(f"An error occurred while appending to the CSV file: {e}")

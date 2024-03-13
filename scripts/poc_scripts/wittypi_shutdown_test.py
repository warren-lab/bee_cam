"""
This script will attempt to shutdown the wittyPi by using our knowledge 
of the i2c and the smbus register...

smbus2 -> https://github.com/kplindegaard/smbus2

Datasheets:
Witty Pi 4 Mini Main Datasheet:
    - https://www.uugear.com/doc/WittyPi4Mini_UserManual.pdf
THE RTC:
    - https://www.nxp.com/docs/en/data-sheet/PCF85063A.pdf
    - NOTE -> Weekdays go from 0 to 6...
        Ex: Weekday transformed from BCD to INT that is 3 corresponds to Wednesday
"""
from smbus2 import SMBus
from datetime import datetime
## i2c Bus 1
## wittypi 4 mini is on
#### device -> x08

# Function to convert Decimal to BCD 
def BCDConversion(n) :
    """
    Function from GeeksforGeeks
    https://www.geeksforgeeks.org/convert-a-given-decimal-number-to-its-bcd-representation/

    """ 
 
    # Base Case 
    if (n == 0) : 
        return "0000"
 
    # To store the reverse of n 
    rev = 0
 
    # Reversing the digits 
    while (n > 0) : 
        rev = rev * 10 + (n % 10)
        n = n // 10

    # Iterate through all digits in rev 
    num = ""
    while (rev > 0) : 
 
        # Find Binary for each digit 
        # using bitset 
        b = str(rev % 10)
         
        # Print the Binary conversion 
        # for current digit 
        # print("{0:04b}".format(int(b, 16)), end = " ") 
        num += "{0:04b}".format(int(b, 16))
        # Divide rev by 10 for next digit 
        rev = rev // 10
    return num
def bcd_to_int(bcd):
    """
    Convert a BCD-encoded number to an integer. 
    """
    return ((bcd & 0xF0) >> 4) * 10 + (bcd & 0x0F)

with SMBus(1) as bus:
    b = bus.read_byte_data(8, 27)
    print(b)
    ## Power Mode? USB c 5v = 0, LDO regulator = 1
    powermode = bus.read_byte_data(8,7)
    print("Power Mode", powermode)
    ## The reason code for latest action
    latest_action = bus.read_byte_data(8,11)
    print("Input Voltage",latest_action)
    # Read RTC time from the WittyPi [IT IS ALREADY IN INT VALUES]
    time_list = []
    for i in range(58,65):

        time_list.append(bcd_to_int(bus.read_byte_data(8,i)))
    print(time_list)
    sec,min,hour,days,weekday,month,year= time_list
    # Python3 program for the above approach 
    print(datetime(year+2000,month,days,hour,min,sec))
    print("Weekday",weekday)
    shutdown_time_min = 5 #minutes
    min_shutdown= min +shutdown_time_min
    shutdown_time_list =[sec,min_shutdown,hour,days,weekday]
    # Okay Schedule the Next Shutdown to be in 5 minutes...
    ## Set Minute  of Alarm2 -> 33 INT TO BCD
    ## Set Hour of Alarm2 -> 34 INT TO BCD
    ## Set Day of Alarm2 -> 35 INT TO BCD
    # ## Set Day of Week of Alarm2 -> 36, INT TO BCD
    for count, val in enumerate(range(32,37)):
        # print(val, shutdown_time_list[count],BCDConversion(shutdown_time_list[count]))
        bus.write_byte_date(8,val,BCDConversion(shutdown_time_list[count]))
    if bcd_to_int(bus.read_byte_data(8,40)) == 0:
        print("ALARM2 AKA SHUTDOWN: NOT TRIGGERED")
    elif bcd_to_int(bus.read_byte_data(8,40)) == 1:
        print("ALARM2 AKA SHUTDOWN: TRIGGERED")
        print("Shutdown Time:\n")
        shut_list = []
        for i in range(32,37):
            shut_list.append(bcd_to_int(bus.read_byte_data(8,i)))
        sec,min,hour,days,weekday,month,year= time_list
        # Python3 program for the above approach 
        print(datetime(day=days,hour = hour,minute=min,second=sec))


    ##  # Using datetime.today()  INT
   


# # Given Number 
# N = 12
 

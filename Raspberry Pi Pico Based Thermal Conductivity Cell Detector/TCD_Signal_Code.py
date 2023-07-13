import machine
from machine import Pin
import utime
key = Pin(0, Pin.IN, Pin.PULL_UP)
# The I2C address of the ADS1115 module is 0x48
ADS1115_ADDR = 0x48
CONFIG_REG = 0x01
# Gain value
GAIN = 4
# Corresponding voltage range
VOLTAGE = 2.048
#Total signal acquisition time, s
Total_time = 6000
# Turn on I2C communication
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=400000)
def set_gain(gain):
    # Get the current configuration
    config = bytearray(2)
    i2c.readfrom_mem_into(ADS1115_ADDR, CONFIG_REG, config)
    # Set the last three digits of the configuration byte to the gain value
    config[0] &= 0b11111000  # Clear the last three digits
    config[0] |= gain & 0b00000111  # Set the gain value
    # Write a new configuration byte
    i2c.writeto_mem(ADS1115_ADDR, CONFIG_REG, config)
    return config

start_time = utime.ticks_ms()
end_time = utime.ticks_ms()
time_elapsed = (end_time - start_time)/1000
#Configure the ADS1115 module to differential input mode and read the voltage values of AIN0 and AIN1
config = set_gain(GAIN)
# Read data from ADS1115 module
# Open the file, 'w' means open the file in write mode
file = open('data.txt', 'w')
# Write the first row of data
data1_1 = 'Time'
data1_2 = 'TCD Signal'
file.write(data1_1+'\t'+data1_2+'\n')
# Close the file
file.close()
while time_elapsed < Total_time:
    end_time = utime.ticks_ms()
    time_elapsed = (end_time - start_time)/1000
    i2c.writeto(ADS1115_ADDR,  config)
    # Send the command to read data
    i2c.writeto(ADS1115_ADDR, bytes([0x00]))
    # Read 2 bytes of data, high byte before, low byte after
    data = i2c.readfrom(ADS1115_ADDR, 2)
    # Convert 2 bytes of data to decimal integers
    value = (data[0] << 8) | data[1]
    # Convert a 16-bit signed number to a signed integer
    if value > 0x7FFF:
        value = value - 0x10000
    # Convert signed integers to voltage values (in mV)
    voltage = value * VOLTAGE / 32768 * 1000
    # Printed Origional Value 
    print("Time: {:.2f} s Value: {:.2f}  Voltage: {:.2f} mV".format(time_elapsed,value,voltage))
    # Wait 0.1 seconds
    utime.sleep_ms(50)

    # Open the file, 'a' means open the file in append mode
    file = open('data.txt', 'a')
    # Write the second row of data
    data2_1 = str(time_elapsed)
    data2_2 = str(voltage)
    file.write(data2_1+'\t'+data2_2+'\n')
    # Close the file
    file.close()
    if key.value() == 0:
        #Read the value of key, i.e. GPIO0, and judge whether it is 0, if it is 0, it means the key is pressed
        utime.sleep_ms(50)
        #Wait for a while and then re-judge to prevent key jitter problems
        if key.value() == 0:
            #The button was indeed pressed
            #Output Information
            print('t0')
            # Open the file, 'a' means open the file in append mode
            file = open('data.txt', 'a')
            file.write('Start:\n')
            # Close the file
            file.close()
            




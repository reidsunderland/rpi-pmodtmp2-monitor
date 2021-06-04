import time
from datetime import datetime
import smbus

NSAMPLES = 10 # number of samples to average for one reading
SAMPLE_DELAY = 0.100 # seconds to delay

addr = 0x4B # i2c address of temperature sensor

# Initialize i2c comms
bus = smbus.SMBus(1)

# Check the config, set to 16 bit mode if needed
config = bus.read_byte_data(addr, 0x03)
print("Read config: {:02X}".format(config))
if (config != 0x80):
    newConfig = config | 0b10000000
    print("Going to write:      {:02X}".format(newConfig))
    bus.write_byte_data(addr, 0x03, newConfig)
    verConfig = bus.read_byte_data(addr, 0x03)
    print("Verified new config: {:02X}".format(verConfig))

# Resolution for 16 bit mode is 0.0078, for 13 bit mode is 0.0625
res = 0.0078

# Get multiple readings
readingSum = 0
for i in range(NSAMPLES):

    # Read 2 bytes starting from offset 0x00
    # 0x00 is temp msb, 0x01 is temp lsb
    val = bus.read_i2c_block_data(addr, 0x00, 2)

    # Combine MSB and LSB
    temp = (val[0] << 8 | val[1])

    # By default, ADC is config for 13 bit so shift right by 3 if needed
    #temp = (temp>>3) * res # res = 0.0625

    # Calculate temp, add to running sum
    readingSum += (temp * res)

# Get time
time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# Get temperature average
temp = readingSum / NSAMPLES

out = "{}, {}".format(time, temp)
print(out)

with open("/home/pi/Documents/temp_log.csv", mode='a') as f:
    f.write(out + "\n")


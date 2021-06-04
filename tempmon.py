import time
from datetime import datetime
import smbus

addr = 0x4B

bus = smbus.SMBus(1)

# Resolution for 16 bit mode is 0.0078, for 13 bit mode is 0.0625
config = bus.read_byte_data(addr, 0x03)
print("Read config: {:02X}".format(config))
if (config != 0x80):
    newConfig = config | 0b10000000
    print("Going to write:      {:02X}".format(newConfig))
    bus.write_byte_data(addr, 0x03, newConfig)
    verConfig = bus.read_byte_data(addr, 0x03)
    print("Verified new config: {:02X}".format(verConfig))

# Read 2 bytes starting from offset 0x00
# 0x00 is temp msb, 0x01 is temp lsb
val = bus.read_i2c_block_data(addr, 0x00, 2)

# Combine MSB and LSB
temp = (val[0] << 8 | val[1])

# By default, ADC is config for 13 bit so shift right by 3 if needed
#temp = (temp>>3) * 0.0625
# res = 0.0625

res = 0.0078

# Calculate temp
temp = temp * res

# Get time
time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

out = "{}, {}".format(time, temp)
print(out)

with open("temp_log.csv", mode='a') as f:
    f.write(out + "\n")


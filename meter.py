import serial

def getLong(data, addr):
    return data[addr]*256*256*256+s[addr+1]*256*256+s[addr+2]*256+s[addr+3]

def getInt(data, addr):
    return data[addr]*256^1+s[addr+1]

# read data from serial port
ser = serial.Serial('/dev/tty.usbserial-A900bZvX', baudrate=19200, timeout=3)
ser.write(bytes([0x77, 0x33, 0xC0, 0x41]))
ser.flush()
s = ser.read(44)
ser.close()

# get sensor readings from raw data
voltage = getLong(s,5)
current = getLong(s,9)
power = getLong(s,13)
usage = getLong(s,17)
loadtime = getLong(s,21)
capacity = getLong(s,25)
cum_usage = getLong(s,29)
cum_capacity = getLong(s,33)
cum_loadtime = getLong(s,37)
temperature = getInt(s,41)
switch = s[43]

# output readings to console
print("Voltage:", voltage/1000, "V")
print("Current:", current/1000, "A")
print("Power:", power/1000, "W")
print("Usage:", usage/1000, "Wh")
print("Loadtime:", loadtime,"min")
print("Capacity:", capacity/1000,"AH")
print("Cummulative Usage:", cum_usage/1000, "Wh")
print("Cummulative Loadtime:", cum_loadtime,"min")
print("Cummulative Capacity:", cum_capacity/1000,"AH")
print("Temperature:", temperature/10,"°C")
print("Switch:", switch)

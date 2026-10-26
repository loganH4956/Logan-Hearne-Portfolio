import time
import board
import digitalio
from adafruit_tca9548a import TCA9548A
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

GPIO0 = digitalio.DigitalInOut(board.D0) # This is a nightmare, I set every GPIO pin to OUTPUT and this sucks but it works
GPIO0.direction = digitalio.Direction.OUTPUT
GPIO1 = digitalio.DigitalInOut(board.D1)
GPIO1.direction = digitalio.Direction.OUTPUT
GPIO4 = digitalio.DigitalInOut(board.D4)
GPIO4.direction = digitalio.Direction.OUTPUT
GPIO5 = digitalio.DigitalInOut(board.D5)
GPIO5.direction = digitalio.Direction.OUTPUT
GPIO6 = digitalio.DigitalInOut(board.D6)
GPIO6.direction = digitalio.Direction.OUTPUT

GPIO7 = digitalio.DigitalInOut(board.D7)
GPIO7.direction = digitalio.Direction.OUTPUT
GPIO8 = digitalio.DigitalInOut(board.D8)
GPIO8.direction = digitalio.Direction.OUTPUT
GPIO9 = digitalio.DigitalInOut(board.D9)
GPIO9.direction = digitalio.Direction.OUTPUT
GPIO10 = digitalio.DigitalInOut(board.D10)
GPIO10.direction = digitalio.Direction.OUTPUT
GPIO11 = digitalio.DigitalInOut(board.D11)
GPIO11.direction = digitalio.Direction.OUTPUT

GPIO12 = digitalio.DigitalInOut(board.D12)
GPIO12.direction = digitalio.Direction.OUTPUT
GPIO13 = digitalio.DigitalInOut(board.D13)
GPIO13.direction = digitalio.Direction.OUTPUT
GPIO14 = digitalio.DigitalInOut(board.D14)
GPIO14.direction = digitalio.Direction.OUTPUT

GPIO15 = digitalio.DigitalInOut(board.D15)
GPIO15.direction = digitalio.Direction.OUTPUT
GPIO16 = digitalio.DigitalInOut(board.D16)
GPIO16.direction = digitalio.Direction.OUTPUT
GPIO17 = digitalio.DigitalInOut(board.D17)
GPIO17.direction = digitalio.Direction.OUTPUT
GPIO18 = digitalio.DigitalInOut(board.D18)
GPIO18.direction = digitalio.Direction.OUTPUT
GPIO19 = digitalio.DigitalInOut(board.D19)
GPIO19.direction = digitalio.Direction.OUTPUT
GPIO20 = digitalio.DigitalInOut(board.D20)
GPIO20.direction = digitalio.Direction.OUTPUT
GPIO21 = digitalio.DigitalInOut(board.D21)
GPIO21.direction = digitalio.Direction.OUTPUT

GPIO15.value = False # ALWAYS KEEP GPIO15-17 LOW
GPIO16.value = False
GPIO17.value = False

GPIO18.value = False # CURRENT CONTROL, KEEP ALL LOW WHEN INITIALIZING (CURRENT 1) (Ideally 1.354uA)
GPIO19.value = False # (CURRENT 2) (Ideally 14.404uA)
GPIO20.value = False # (CURRENT 3) (Ideally 1.354mA)
GPIO21.value = False # (CURRENT 4) (Ideally 6.77mA)

GPIO12.value = False # ALWAYS KEEP LOW
GPIO13.value = False # ALWAYS KEEP LOW
GPIO14.value = False # LATCH PIN, KEEP LOW WHEN SETTING MUX PINS
time.sleep(0.1) # Wait for latch to disable

GPIO0.value = False # MUX1 CONTROL
GPIO1.value = False
GPIO4.value = False
GPIO5.value = False
GPIO6.value = False

GPIO7.value = False # MUX2 CONTROL
GPIO8.value = False
GPIO9.value = False
GPIO10.value = False
GPIO11.value = False

time.sleep(0.1) # Wait for everything to settle
GPIO14.value = True # LATCH MUX PINS

time.sleep(1) # Wait for everything to settle

i2c = board.I2C()

# i2c = busio.I2C(board.SCL, board.SDA)
tca = TCA9548A(i2c)

ads1 = ADS1115(tca[0]) # All of our ADS1115s are on the same address, so we have to use a MUX to select them.
ads2 = ADS1115(tca[1])
ads3 = ADS1115(tca[2])
ads4 = ADS1115(tca[3])
ads5 = ADS1115(tca[4])
ads6 = ADS1115(tca[5])
ads7 = ADS1115(tca[6])
ads8 = ADS1115(tca[7])

ads_list = [ads1, ads2, ads3, ads4, ads5, ads6, ads7, ads8] # Used in read_voltage for efficiency

def mux_enable(mux1, mux2):
    mux1 -= 1 # Convert to 0-indexed
    mux2 -= 1

    GPIO14.value = False # Disable Latch

    time.sleep(0.1) # Wait for latch to disable

    GPIO0.value = mux1 & 0b00001
    GPIO1.value = mux1 & 0b00010
    GPIO4.value = mux1 & 0b00100
    GPIO5.value = mux1 & 0b01000
    GPIO6.value = mux1 & 0b10000

    GPIO7.value = mux2 & 0b00001
    GPIO8.value = mux2 & 0b00010
    GPIO9.value = mux2 & 0b00100
    GPIO10.value = mux2 & 0b01000
    GPIO11.value = mux2 & 0b10000

    time.sleep(0.1) # Wait for MUX pins to settle

    GPIO14.value = True # Latch MUX Pins

def read_voltage(pin): # Returns voltage on pin.
    pin -= 1 # Convert to 0-indexed
    ads_select = ads_list[pin // 4]
    pin %= 4
    match (pin):
        case 0:
            channel = AnalogIn(ads_select, ads1x15.Pin.A0)
        case 1:
            channel = AnalogIn(ads_select, ads1x15.Pin.A1)
        case 2:
            channel = AnalogIn(ads_select, ads1x15.Pin.A2)
        case 3:
            channel = AnalogIn(ads_select, ads1x15.Pin.A3)
        case _:
            raise ValueError("ERROR: Invalid pin number")
    return channel.voltage

def enable_current(current):
    match current:
        case 0:
            GPIO18.value = False
            GPIO19.value = False
            GPIO20.value = False
            GPIO21.value = False
            return 0
        case 1:
            GPIO19.value = False
            GPIO20.value = False
            GPIO21.value = False
            GPIO18.value = True
            # return 1.354 * 10**-6 # Calculated Current
            return 1.22525 * 10**-6 # Measured Current
        case 2:
            GPIO18.value = False
            GPIO20.value = False
            GPIO21.value = False
            GPIO19.value = True
            # return 14.404 * 10**-6 # Calculated Current
            return 14.1748 * 10**-6 # Measured Current
        case 3:
            GPIO18.value = False
            GPIO19.value = False
            GPIO21.value = False
            GPIO20.value = True
            return 1.354 * 10**-3 # Calculated Current
            # return 1.354 * 10**-3 # Measured Current
        case 4:
            GPIO18.value = False
            GPIO19.value = False
            GPIO20.value = False
            GPIO21.value = True
            # return 6.77 * 10**-3 # Calculated Current
            return 7.195 * 10**-3 # Measured Current
        case _:
            raise ValueError("ERROR: Invalid current setting")
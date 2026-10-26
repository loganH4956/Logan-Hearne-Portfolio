import time
from pydantic import BaseModel, Field, ValidationError
import numpy as np
import json
from pathlib import Path
import board
import digitalio
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15
CONFIG = Path(__file__).with_name("burninConfig.json")

i2c = board.I2C()
ads1 = ADS1115(i2c, address=0x48)
ads2 = ADS1115(i2c, address=0x49)

def read_voltage(pad):
    channel = []
    channel.append() = AnalogIn(ads1, ads1x15.Pin.A0) # A
    channel.append() = AnalogIn(ads1, ads1x15.Pin.A1) # B
    channel.append() = AnalogIn(ads1, ads1x15.Pin.A2) # C
    channel.append() = AnalogIn(ads1, ads1x15.Pin.A3) # F
    channel.append() = AnalogIn(ads2, ads1x15.Pin.A0) # G
    channel.append() = AnalogIn(ads2, ads1x15.Pin.A1) # H
    channel.append() = AnalogIn(ads2, ads1x15.Pin.A2) # L
    channel.append() = AnalogIn(ads2, ads1x15.Pin.A3) # GND
    return channel[pad].voltage

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

def configure_pads(pad):
    if pad == 'A':
        GPIO4.value = True
    elif pad =='B':
        GPIO5.value = True
    elif pad == 'C':
        GPIO6.value = True
    elif pad == 'D':
        GPIO11.value = True
    elif pad == 'E':
        GPIO12 = True
    elif pad == 'F':
        GPIO7 = True
    elif pad == 'G':
        GPIO8 = True
    elif pad == 'H':
        GPIO9 = True
    elif pad =='I':
        GPIO13 = True
    elif pad == 'J':
        GPIO14 = True
    elif pad == 'K':
        GPIO15 = True
    elif pad == 'L':
        GPIO10 = True
    elif pad == 'M':
        GPIO16 = True
    elif pad == 'N':
        GPIO17 = True
    elif pad == 'deactivate':
        GPIO4.value = False
        GPIO5.value = False
        GPIO6.value = False
        GPIO7.value = False
        GPIO8.value = False
        GPIO9.value = False
        GPIO10.value = False
        GPIO11.value = False
        GPIO12.value = False
        GPIO13.value = False
        GPIO14.value = False
        GPIO15.value = False
        GPIO16.value = False
        GPIO17.value = False
    else:
        raise ValueError("Incorrect Pad Selection")
    
def enable_current(pad1, pad2):
    configure_pads(pad1)
    configure_pads(pad2)

def disable_current():
    configure_pads('deactivate')

class BurnInConfig(BaseModel):
    pad1: str
    pad2: str
    
    deltar: float = Field(default=CONFIG.DEFAULT_RESISTANCE_DELTA, gt=0)
    on_time: float = Field(default=CONFIG.DEFAULT_CURRENT_ON_TIME, gt=0)
    off_time: float = Field(default=CONFIG.DEFAULT_CURRENT_OFF_TIME, ge=0) # ge=0 means >= 0
    pulses: int = Field(default=CONFIG.DEFAULT_PULSE_NUMBER, gt=0)
    current_setting = int

def measure_resistance(config: BurnInConfig):
    voltage = read_voltage(config.pin1) - read_voltage(config.pin2)
    current = config.current_setting
    if voltage < 0.001:
        return 0
    else:
        return (voltage / current)

def run_burnin(config: BurnInConfig):
    enable_current(config.pad1, config.pad2)

    start_time = time.time()
    initial_res = measure_resistance()

    for i in range(0,config.pulses):

        try:
            while True:
                elapsed_time = time.time() - start_time

                if elapsed_time >= config.on_time:
                    print("Burn-In duration reached")
                    break

                current_resistance = measure_resistance() 

                yield elapsed_time, current_resistance

                res_delta = abs(current_resistance - initial_res)
                if res_delta > config.deltar:
                    print(f"Resistance changed by {res_delta:.2f} Ohms Burn-In canceled")
                    break

                time.sleep(0.1)

        finally:
            disable_current()
            print(f"Initializing lockout for {config.off_time} seconds")
            time.sleep(config.off_time)
            print("Lockout complete")

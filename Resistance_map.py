from functions import enable_current, mux_enable, read_voltage, ads_list

import numpy as np
from openpyxl import Workbook, load_workbook
from datetime import date
import os
import random
import time




"""
# ---------------- Test Mode ----------------
TEST_MODE = True
"""

def b_to_c(b):
    c = ((b % 2) * ((b + 1) / 2)) + (((b + 1) % 2) * (29 - (b / 2)))
    return (int (c))

def c_to_b(c):
    b = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
    return b[c - 1]

#function to measure resistance
def measure_resistance(pin1, pin2, current_setting):
    if (pin1 == 0 and pin2 == 0) or (pin1 == pin2):
        # DEBUG
        current = enable_current(0)
        time.sleep(0.02)
        mux_enable(1, 1)
        time.sleep(0.02)
        voltage = read_voltage(1) - read_voltage(1)
        time.sleep(0.02)
        voltage = read_voltage(1) - read_voltage(1)
        time.sleep(0.02)
        return 0
    
    current = enable_current(0)
    time.sleep(0.02)

    match current_setting:
        case 0:
            for ads in ads_list:
                ads.gain = 16 # Resolution of 7.8125uV, Max Voltage of 0.256V
        case 1:
            for ads in ads_list:
                ads.gain = 1 # Resolution of 125uV, Max Voltage of 4.096V
        case 2:
            for ads in ads_list:
                ads.gain = 2 # Resolution of 62.5uV, Max Voltage of 2.048V
        case 3:
            for ads in ads_list:
                ads.gain = 4 # Resolution of 31.25uV, Max Voltage of 1.024V
        case 4:
            for ads in ads_list:
                ads.gain = 16 # Resolution of 7.8125uV, Max Voltage of 0.256V
        case _:
            raise ValueError("ERROR: Invalid current setting")
    time.sleep(0.02)

    current = enable_current(current_setting)
    time.sleep(0.02)

    mux_enable(pin1, pin2)
    time.sleep(0.01)
    voltage = read_voltage(pin1) - read_voltage(pin2)
    if voltage < 0.001:
        return 0
    else:
        measure_resistance(0, 0, 0) # Phantom Measurement

        return (voltage / current)

#output = np.array([])
results = []

'''
for i in range(1,29):
    print(f"{i} -> {b_to_c(i)} -> {c_to_b(b_to_c(i))}")
'''


"""
def generate_test_matrix():
    data_2d = []

    header_row = [""] + list(range(1,29))
    data_2d.append(header_row)

    counter = 1
    for i in range(28):
        row = [i + 1]
        for j in range(28):
            if j < i:
                row.append(None)
            else:
                row.append(counter)
                counter += 1
        data_2d.append(row)

    return data_2d
"""



def run_resistance_map():
    """
    if TEST_MODE:
        print("Running in TEST MODE — returning simulated resistance matrix")
        return generate_test_matrix()
    """
    results = []
    data_2d = []
    
    header_row = [""] + list(range(1,29))
    data_2d.append(header_row)
    
    resistance_matrix = [[None for _ in range(28)] for _ in range(28)]
    
    #main loop
    for i in range(1,29):
        results.append((i, i, 0.0000))
        resistance_matrix[i - 1][i - 1] = 0.0000

        for j in range(i,29):
            for c in range(1,5):
                res = measure_resistance(c_to_b(i), c_to_b(j), c)
                if res != 0:
                    results.append((i, j, res))
                    resistance_matrix[i - 1][j - 1] = res
                    break
                else:
                    continue

            if resistance_matrix[i - 1][j - 1] is None:
                resistance_matrix[i - 1][j - 1] = 0.0000

    for i in range(28):
        row = [i + 1] + resistance_matrix[i]
        data_2d.append(row)

    for i, j, res in results:
        print(f"Pins ({(i)}, {j}): {res:.4f} Ω")

    return data_2d
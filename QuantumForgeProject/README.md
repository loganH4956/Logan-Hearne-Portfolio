# Atom Chip Automated Test Controller

A Python-based hardware-in-the-loop testing suite with a desktop GUI, designed to perform automated 28x28 resistance mapping and pulsed current burn-in testing on QForge hardware. 

## Overview

This project interfaces standard desktop environments with low-level GPIO and I2C hardware. It controls programmable current sources, routes signals via multiplexers, and reads high-precision voltages across an array of 28 test pads to validate component integrity and track degradation under stress.

### Core Capabilities
* **Hardware Interfacing:** Controls a TCA9548A I2C multiplexer routing to eight 16-bit ADS1115 ADCs, alongside dynamic GPIO latching for pad selection and current sourcing.
* **Automated Resistance Mapping:** Iterates through all combinations of 28 test pins to generate a full cross-resistance matrix, applying phantom measurements and dynamic gain adjustments for high accuracy.
* **Pulsed Burn-In Testing:** Executes stress tests using configurable pulse counts, active duration (`on_time`), and lockout periods (`off_time`), while monitoring real-time resistance drift against safety thresholds ($\pm 10\%$).
* **Desktop GUI & Live Telemetry:** A threaded Tkinter interface prevents UI locking during hardware execution, providing live Matplotlib graphs of cycle-over-cycle resistance and automated Excel report generation with conditional formatting.

## Software Architecture

The codebase separates the frontend UI from hardware execution to ensure timing accuracy and prevent thread-blocking during long burn-in cycles.

* **`GUI.py`:** Main Tkinter application. Handles multithreaded task queues, `matplotlib` embedding, and `.xlsx` generation via `openpyxl`.
* **`functions.py`:** Low-level hardware drivers. Manages the `adafruit_ads1x15` and `adafruit_tca9548a` libraries, calculates measured vs. ideal currents, and handles GPIO latching.
* **`Resistance_map.py`:** Implements the $O(N^2)$ traversal algorithm to map all 28 pins, configuring ADC gain dynamically based on current requirements.
* **`burnin.py`:** Uses `pydantic` for strict configuration validation and operates a generator-based state machine to yield live telemetry back to the GUI.

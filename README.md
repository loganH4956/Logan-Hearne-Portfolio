# Logan Hearne – Technical Portfolio

Welcome to my project repository. I am a student at the University of Colorado Boulder studying computer science, physics, statistics, and astronomy. This repository serves as a central archive for my technical projects, spanning computational physics, hardware-in-the-loop automation, data science, and graphical application development.

---

## Featured Projects

### 1. [Relativistic Cosmic Ray Shower Simulation](./cosmic-ray-simulation)
**Domain:** Computational Physics, Monte Carlo Simulation, Kinematics
* **Overview:** A custom Monte Carlo engine modeling the atmospheric attenuation, two-body decay ($\pi \rightarrow \mu + \nu$), and hadronic downscattering of high-energy galactic protons. 
* **Key Features:** Implements vectorized relativistic reference frame transformations, computes stochastic interaction probabilities based on proper lifetime and altitude, and mathematically demonstrates atmospheric time dilation.
* **Tech Stack:** Python, NumPy, Matplotlib, Jupyter Notebook.

### 2. [QForge Automated Hardware Test Controller](./qforge-test-controller)
**Domain:** Hardware-in-the-Loop (HITL) Testing, Embedded Systems, GUI Development
* **Overview:** A multithreaded desktop application designed to interface with a custom PCB test bench for programmable current sourcing and 28x28 resistance mapping.
* **Key Features:** Controls an I2C multiplexer (TCA9548A) and eight 16-bit ADCs (ADS1115) to read micro-volt differentials. Includes a Tkinter GUI with real-time Matplotlib telemetry to run cyclical stress tests and automatically halt upon detecting threshold-exceeding resistance degradation. 
* **Tech Stack:** Python, Tkinter, Matplotlib, OpenPyXL, Pydantic, Blinka (Raspberry Pi GPIO/I2C).

---

## Additional Work & Archives

* **[Data Science & Analysis](./data-science-archive):** Contains academic research and data cleaning scripts, including a study on electric vehicle trends in Washington State and Pandas-based administrative pipelines.
* **[Systems & Low-Level Programming](./systems-programming):** Coursework exploring x86-64 assembly, memory layout, stack mechanics, and ELF object symbol tables.
* **[Quantum Computing](./quantum-computing):** Exploratory projects utilizing Qiskit for quantum circuit implementation and simulation.

---

## Technical Toolbox

* **Languages:** Python, SQL, C/C++, x86-64 Assembly, JavaScript
* **Libraries & Frameworks:** NumPy, SciPy, Pandas, Matplotlib, Tkinter, Qiskit, Pydantic
* **Hardware & Embedded:** I2C/SPI interfaces, GPIO routing, ADC multiplexing, basic oscilloscope/multimeter troubleshooting
* **Tools & Environment:** Git, Linux, Jupyter, LaTeX, GitHub Actions

---

A Python-based design automation tool for calculating Charge Pump Phase-Locked Loop (CP-PLL) loop filter components. This script utilizes geometric mean optimization to determine the optimal capacitor ratio and spread factor based on a target phase margin, making it highly useful for analog and mixed-signal IC design workflows.

## Features
* **Geometric Mean Optimization:** Calculates the ideal capacitor ratio (C1/C2) and spread factor to maximize phase margin.
* **Component Sizing:** Automatically computes the required values for R1, C1, and C2 based on given system-level constraints (Loop Bandwidth, Charge Pump Current, VCO Gain, and Divider Ratio).
* **Data Visualization:** Generates an annotated plot visualizing the relationship between the Capacitor Ratio and Phase Margin.
* **Pole/Zero Extraction:** Outputs the exact frequency locations of the stabilizing zero and the third pole.

## Prerequisites
To run this script, you need Python installed along with the following libraries:
* `numpy`
* `matplotlib`

You can install them via pip:
```bash
pip install numpy matplotlib

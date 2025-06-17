# Grover-Based Quantum Algorithms for Protein Design

This repository contains the Python code used in our paper:  
**"Quantum Circuits for Protein Design using Grover’s Algorithm"**  
Published in *PLOS Computational Biology*  
👉 [Read the paper here](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011033)

## Requirements

- **Python version:** 3.8.2  
- **Qiskit version:** 0.24.0  

To install a specific Qiskit version, [this YouTube guide](https://www.youtube.com/watch?v=L1TPD43UTZM) may be helpful.

Expected runtime and resource requirements are provided in the supplementary materials of the paper.

---

## Code Structure

The repository is organized into two models:

### 1. SP Model (Single Precision)

Directory: `codes/SP-model/`

- **Core functions:**  
  `functions_ripple_carry_adder_E8.py` includes all necessary functions for the SP model circuits.

- **File naming convention:**  
  Example: `2res-1inter-m4-iter-1-E2.py`  
  - `2res`: 2 designable sites  
  - `1inter`: 1 interaction  
  - `m4`: m = 4  
  - `iter-1`: R = 1 iteration  
  - `E2`: Energy threshold = 2

- **Expected output example:**  
  `SP-3res-2inter-m5-iter-1-E7.txt` contains expected output for `3res-2inter-m5-iter-1-E7.py`

---

### 2. MR Model (Mixed Resolution)

Directory: `codes/MR-model/`

- **Core functions:**  
  `func_apr_20_2021_decim_E_dec.py` includes all necessary functions for the MR model circuits.

- **File naming convention:**  
  Example: `3r_3c_4i5d_r1_e.70.py`  
  - `3r`: 3 designable sites  
  - `3c`: 3 interactions  
  - `4i5d`: 4 qubits for integer part, 5 for decimal  
  - `r1`: R = 1 iteration  
  - `e.70`: Energy threshold = 70% of minimum energy

- **Expected output example:**  
  `MR_s3_i3_m9p5_R1_Eth80.txt` contains expected output for `3r_3c_4i5d_r1_e.80.py`

---

## Abstract

Protein design is a technique to engineer proteins by permuting amino acids in the sequence to obtain novel functionalities. However, exploring all possible combinations of amino acids is generally impossible due to the exponential growth of possibilities with the number of designable sites. The present work introduces circuits implementing a pure quantum approach, Grover’s algorithm, to solve protein design problems. Our algorithms can adjust to implement any custom pairwise energy tables and protein structure models. Moreover, the algorithm’s oracle is designed to consist of only adder functions. Quantum computer simulators validate the practicality of our circuits, containing up to 234 qubits. A smaller circuit is also implemented on real quantum devices. Our results show that using \( R \) iterations, the circuits find the correct results among all \( N \) possibilities, providing the expected quadratic speed-up of Grover’s algorithm over classical methods.

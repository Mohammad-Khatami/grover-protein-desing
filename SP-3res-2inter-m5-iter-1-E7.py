#!/usr/bin/env python

#initialization
#import matplotlib.pyplot as plt
#import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library.standard_gates import UGate
from qiskit.circuit.library.standard_gates import *
from qiskit.quantum_info import Statevector
from qiskit.providers.aer import QasmSimulator

# import basic plot tools
from qiskit.visualization import plot_histogram
from functions_ripple_carry_adder_E8 import diffuser, add, add_dg, energy, energy_dg

######################### 
######################### 
######################### 
 
#       O---1    
#       |          
#       2   0---O    
 
######################### 
######################### 
######################### 

# Create separate registers to name bits
# Create separate registers to name bits
iteration=1  # number of iterations
num_res=3    # s=3 number of designable sites
num_q_for_res=3  #number of g (qubits for representing residues)
n=num_res*num_q_for_res   # number of n
m=5                       # number of m qubits in the work qubits
var_qubits = QuantumRegister(n, name='res') # all n qubits
a_qubits = QuantumRegister(m, name='a')     # qubits in the work qubits
b_qubits = QuantumRegister(m, name='b')     # qubits in the work qubits
o_qubits = QuantumRegister(1, name='output')  # bits to store clause-checks
classic_bits = ClassicalRegister(n, name='classic')  # bits to store clause-checks

qc_w = QuantumCircuit(var_qubits,a_qubits,b_qubits,o_qubits,classic_bits)

#initialization with Hadamard gates!
for i in range(n):
    qc_w.h(var_qubits[i])
qc_w.barrier()

################################################################
for i in range(iteration):            # number of iterations for Oracle and Diffuser
    energy(qc_w,0,1,0,m,var_qubits,a_qubits)#bond a to ene_a  
    energy(qc_w,0,2,0,m,var_qubits,b_qubits)#bond b to ene_b  
    add(qc_w,a_qubits,b_qubits,o_qubits,m)#sum inteaction A and B  -> b_qubit  
    energy_dg(qc_w,0,1,0,m,var_qubits,a_qubits)# clean A form a_qubits to put E_th!
    ##E_th -7
    qc_w.x(a_qubits[0])
    qc_w.x(a_qubits[1])
    qc_w.x(a_qubits[2])
    ## now sum!
    add(qc_w,b_qubits,a_qubits,o_qubits,m) 
    ###activate out!
    qc_w.x(o_qubits)
    ###calcullator; now checks if answer is negative or not
    ###############################################################
    qc_w.cz(a_qubits[m-1],o_qubits[0])
    ############ Now clean up!
    qc_w.x(o_qubits)
    add_dg(qc_w,b_qubits,a_qubits,o_qubits,m) 
    ##E_th= -7
    qc_w.x(a_qubits[0])
    qc_w.x(a_qubits[1])
    qc_w.x(a_qubits[2])
    energy(qc_w,0,1,0,m,var_qubits,a_qubits)# clean A form a_qubits
    add_dg(qc_w,a_qubits,b_qubits,o_qubits,m)#sum A+B -> b_qubit  
    energy_dg(qc_w,0,2,0,m,var_qubits,b_qubits)#bond b to ene_b  
    energy_dg(qc_w,0,1,0,m,var_qubits,a_qubits)#bond a to ene_a 
    # ##############################################################
    # ###Diffuser
    # ##############################################################
    qc_w.append(diffuser(n), list(range(n)))
    qc_w.barrier()

#measurement
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###########
# qc_w.barrier()
for j in range(n):
    qc_w.measure(var_qubits[j],classic_bits[j])


#qc_w.draw('mpl')     # uncomment to show the circuit 
###########################
### the simulator!
###########################
matrix_simulator = QasmSimulator(method='matrix_product_state')
result = execute(qc_w, matrix_simulator, shots=1000000).result()
data=result.get_counts()
print('1000000 shots in {}s'.format(result.time_taken))

# save output in text file!
with open('SP-3res-2inter-m5-iter-1-E7.txt', 'w') as file:
    file.write(str(data))


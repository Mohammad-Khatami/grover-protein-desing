#!/usr/bin/env python

#initialization
import matplotlib.pyplot as plt
import numpy as np

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

#         
#    O---2---4   
#                 
#    1---3---5   
#        


# Create separate registers to name bits
# Create separate registers to name bits
iteration=1
num_res=6
num_q_for_res=3
n=num_res*num_q_for_res
m=6
var_qubits = QuantumRegister(n, name='res') 
a_qubits = QuantumRegister(m, name='a')
b_qubits = QuantumRegister(m, name='b') 
c_qubits = QuantumRegister(m, name='c') 
# sum_aux_b_qubits = QuantumRegister(m, name='sum_aux_b') 
# sum_aux_c_qubits = QuantumRegister(m, name='sum_aux_c') 
# aux_qubits = QuantumRegister(2, name='aux')  
o_qubits = QuantumRegister(1, name='output')  # bits to store clause-checks
classic_bits = ClassicalRegister(n, name='classic')  # bits to store clause-checks

qc_w = QuantumCircuit(var_qubits,a_qubits,b_qubits,o_qubits,classic_bits)

#var!
for i in range(n):
    qc_w.h(var_qubits[i])
qc_w.barrier()

################################################################
for i in range(iteration):
    energy(qc_w,0,1,0,m,var_qubits,a_qubits)#bond a to ene_a  
    energy(qc_w,2,3,0,m,var_qubits,b_qubits)#bond b to ene_b  
    add(qc_w,a_qubits,b_qubits,o_qubits,m)#sum A+B -> b_qubit  
    energy_dg(qc_w,0,1,0,m,var_qubits,a_qubits)# clean A form a_qubits
    energy(qc_w,4,5,0,m,var_qubits,a_qubits)#bond C -> a_qubits  
    add(qc_w,a_qubits,b_qubits,o_qubits,m)# add A+B+C -> A
    energy_dg(qc_w,4,5,0,m,var_qubits,a_qubits)# clean A form a_qubits
    ##thrsh -10
    #qc_w.x(a_qubits[0])
    qc_w.x(a_qubits[1])
    qc_w.x(a_qubits[3])
    ## now sum!
    add(qc_w,b_qubits,a_qubits,o_qubits,m) 
    ###activate out!
    qc_w.x(o_qubits)
    ###calcullator; now checks if sum_aux_a_qubits is negative or not
    ###############################################################
    qc_w.cz(a_qubits[m-1],o_qubits[0])
    ############
    qc_w.x(o_qubits)
    add_dg(qc_w,b_qubits,a_qubits,o_qubits,m) 
    ##thrsh -10
    #qc_w.x(a_qubits[0])
    qc_w.x(a_qubits[1])
    qc_w.x(a_qubits[3])
    energy(qc_w,4,5,0,m,var_qubits,a_qubits)# clean A form a_qubits
    add_dg(qc_w,a_qubits,b_qubits,o_qubits,m)# add A+B+C -> A
    energy_dg(qc_w,4,5,0,m,var_qubits,a_qubits)#bond C -> a_qubits  
    energy(qc_w,0,1,0,m,var_qubits,a_qubits)# clean A form a_qubits
    add_dg(qc_w,a_qubits,b_qubits,o_qubits,m)#sum A+B -> b_qubit  
    energy_dg(qc_w,2,3,0,m,var_qubits,b_qubits)#bond b to ene_b  
    energy_dg(qc_w,0,1,0,m,var_qubits,a_qubits)#bond a to ene_a  

    # ###Diffuser
    # ##############################################################
    qc_w.append(diffuser(n), list(range(n)))
    qc_w.barrier()

#measure!
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###########
# qc_w.barrier()
for j in range(n):
    qc_w.measure(var_qubits[j],classic_bits[j])


#qc_w.draw('mpl')
#qasm_simulator = Aer.get_backend('qasm_simulator')
#result = execute(qc_w, backend=qasm_simulator, shots=1000000).result()


matrix_simulator = QasmSimulator(method='matrix_product_state')
result = execute(qc_w, matrix_simulator, shots=1000000).result()
data=result.get_counts()
print('1000000 shots in {}s 1-iter'.format(result.time_taken))

with open('6res-3inter-m6-iter-1-E10.txt', 'w') as file:
    file.write(str(data))


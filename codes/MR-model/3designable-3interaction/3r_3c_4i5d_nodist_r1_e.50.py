#!/usr/bin/env python
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library.standard_gates import UGate
from qiskit.circuit.library.standard_gates import *
from qiskit.quantum_info import Statevector
from qiskit.providers.aer import QasmSimulator
#from func_apr_12_2021_decim import *
from func_apr_20_2021_decim_E_dec import *

##############################
iteration=1
num_res=3
num_q_for_res=3
n=num_res*num_q_for_res
num_int=4;
num_dec=5;
m=num_int+num_dec
#it=int((num_res*(num_res-1))/2
##E

var_qubits = QuantumRegister(n, name='res')
a_qubits = QuantumRegister(m, name='a')
b_qubits = QuantumRegister(m, name='b')

o_qubits = QuantumRegister(1, name='ancila') 
classic_bits = ClassicalRegister(n, name='classic')  # bits to store clause-checks
#qc_dist = QuantumCircuit(var_qubits,a_qubits,b_qubits,c_qubits,d_qubits,rx_qubits,ry_qubits,rz_qubits,
#                        mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,classic_bits)
qc_dist = QuantumCircuit(var_qubits,a_qubits,b_qubits,o_qubits,classic_bits)
thrsh=4.3*.5
####### H-gates!
####### H-gates!
qc_dist.h(var_qubits)
######################################## Now grover! 
for i in range(iteration):
    ene_8(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## A-->a
    #####
    ene_8(qc_dist,0,2,var_qubits,b_qubits,8,num_q_for_res,num_int,num_dec)## B-->a
    ####
    add(qc_dist,a_qubits,b_qubits,o_qubits,m) ###C*d_c >>d
    ####
    ene_8_dg(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## A-->a
    ene_8(qc_dist,1,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## C-->a
    add(qc_dist,a_qubits,b_qubits,o_qubits,m) ###C*d_c >>d
    ene_8_dg(qc_dist,1,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## C-->a
    ####
    ####Thresh
    binnary(qc_dist,thrsh,a_qubits,num_int,num_dec)
    add(qc_dist,a_qubits,b_qubits,o_qubits,m)
    ###activate out!
    qc_dist.x(o_qubits[0])
    ###calcullator; now checks if qubits are negative or not
    qc_dist.cz(b_qubits[m-1],o_qubits[0])
    ############
    qc_dist.x(o_qubits[0])
    #####
    add_dg(qc_dist,a_qubits,b_qubits,o_qubits,m)
    binnary_dg(qc_dist,thrsh,a_qubits,num_int,num_dec)
    ene_8(qc_dist,1,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## C-->a
    add_dg(qc_dist,a_qubits,b_qubits,o_qubits,m) ###C*d_c >>d
    ene_8_dg(qc_dist,1,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## C-->a
    ene_8(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## A-->a
    add_dg(qc_dist,a_qubits,b_qubits,o_qubits,m) ###C*d_c >>d
    ene_8_dg(qc_dist,0,2,var_qubits,b_qubits,8,num_q_for_res,num_int,num_dec)## B-->a
    ene_8_dg(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## A-->a

    ######
    qc_dist.append(diffuser(n), list(range(n)))
########## measure
qc_dist.measure(var_qubits,classic_bits)

###########simulator
matrix_simulator = QasmSimulator(method='matrix_product_state')
result = execute(qc_dist, matrix_simulator, shots=1000000,max_parallel_threads=0).result()
data=result.get_counts()
print('1000000 shots in {} s'.format(result.time_taken))
print('Ennergy thresh was {} E'.format(thrsh))
#print (data)
with open('3r_3c_4i5d_nodist_r1_e.50.txt', 'w') as file:
    file.write(str(data))


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
num_dec=10;
m=num_int+num_dec
#it=int((num_res*(num_res-1))/2
##E

var_qubits = QuantumRegister(n, name='res')
a_qubits = QuantumRegister(m, name='a')
b_qubits = QuantumRegister(m, name='b')
c_qubits = QuantumRegister(m, name='c')
d_qubits = QuantumRegister(m, name='d')
#e_qubits = QuantumRegister(m, name='e')
#rx_qubits = QuantumRegister(m, name='rx')
#ry_qubits = QuantumRegister(m, name='ry')
#rz_qubits = QuantumRegister(m, name='rz')
mp_qubits=QuantumRegister(4*m, name='mp')
mp_res_qubits=QuantumRegister(4*m, name='mp_res')

a_ext_qubits = QuantumRegister(2*m, name='a_ext')
b_ext_qubits = QuantumRegister(2*m, name='b_ext')

o_qubits = QuantumRegister(1, name='ancila') 
classic_bits = ClassicalRegister(n, name='classic')  # bits to store clause-checks
#qc_dist = QuantumCircuit(var_qubits,a_qubits,b_qubits,c_qubits,d_qubits,rx_qubits,ry_qubits,rz_qubits,
#                        mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,classic_bits)
qc_dist = QuantumCircuit(var_qubits,a_qubits,b_qubits,c_qubits,d_qubits,mp_qubits,
                        mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,classic_bits)
##########################################initiation 

#######
#######input the 1/d
#######
#inv_d=[0.3507153119159472, 0.4163054471218132, 1.4142135623730951]
#inv_d=[0.3507153119159472, 0.24992191160203064, 0.7495316889958613]
inv_d=[0.2204869318512118, 0.16881394379731987, 0.45454545454545453]
t=0
for i in range (len(inv_d)):
    t=t+inv_d[i]
thrsh=t*4.3*.7
####### H-gates!
####### H-gates!
qc_dist.h(var_qubits)
######################################## Now grover! 
for i in range(iteration):
    ene_8(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## A-->a
    binnary(qc_dist,inv_d[0],b_qubits,num_int,num_dec)##d_a -->b
    multiply_same(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##A*d_a -->c
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add(qc_dist,c_qubits,d_qubits,o_qubits,m) ###A*d_a >>d
    multiply_same_dg(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##c clean
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    binnary_dg(qc_dist,inv_d[0],b_qubits,num_int,num_dec)##d_a clean
    ene_8_dg(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec) ##a clean
    #####
    ene_8(qc_dist,0,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## B-->a
    binnary(qc_dist,inv_d[1],b_qubits,num_int,num_dec)##d_b -->b
    multiply_same(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##B*d_b -->c
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add(qc_dist,c_qubits,d_qubits,o_qubits,m) ###B*d_b >>d
    multiply_same_dg(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,## c clean
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    binnary_dg(qc_dist,inv_d[1],b_qubits,num_int,num_dec)##d_b clean
    ene_8_dg(qc_dist,0,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec) ##B clean
    ####
    ene_8(qc_dist,1,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## C-->a
    binnary(qc_dist,inv_d[2],b_qubits,num_int,num_dec)##d_c -->b
    multiply_same(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##C*d_c -->c
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add(qc_dist,c_qubits,d_qubits,o_qubits,m) ###C*d_c >>d
    binnary_dg(qc_dist,inv_d[2],b_qubits,num_int,num_dec)##b clean
    ####
    ####Thresh
    binnary(qc_dist,thrsh,b_qubits,num_int,num_dec)
    add(qc_dist,d_qubits,b_qubits,o_qubits,m)
    ###activate out!
    qc_dist.x(o_qubits[0])
    ###calcullator; now checks if qubits are negative or not
    qc_dist.cz(b_qubits[m-1],o_qubits[0])
    ############
    qc_dist.x(o_qubits[0])
    add_dg(qc_dist,d_qubits,b_qubits,o_qubits,m)
    binnary_dg(qc_dist,thrsh,b_qubits,num_int,num_dec)
    ####Thresh
    ####
    binnary(qc_dist,inv_d[2],b_qubits,num_int,num_dec)##b clean
    add_dg(qc_dist,c_qubits,d_qubits,o_qubits,m) ###C*d_c >>d
    multiply_same_dg(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##C*d_c -->c
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    binnary_dg(qc_dist,inv_d[2],b_qubits,num_int,num_dec)##d_c -->b
    ene_8_dg(qc_dist,1,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## C-->a
    ###
    ene_8(qc_dist,0,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec) ##B clean
    binnary(qc_dist,inv_d[1],b_qubits,num_int,num_dec)##d_b clean
    multiply_same(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,## c clean
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add_dg(qc_dist,c_qubits,d_qubits,o_qubits,m) ###B*d_b >>d
    multiply_same_dg(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##B*d_b -->c
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    binnary_dg(qc_dist,inv_d[1],b_qubits,num_int,num_dec)##d_b -->b
    ene_8_dg(qc_dist,0,2,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## B-->a
    ####
    ene_8(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec) ##a clean
    binnary(qc_dist,inv_d[0],b_qubits,num_int,num_dec)##d_a clean
    multiply_same(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##c clean
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add_dg(qc_dist,c_qubits,d_qubits,o_qubits,m) ###A*d_a >>d
    multiply_same_dg(qc_dist,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,##A*d_a -->c
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    binnary_dg(qc_dist,inv_d[0],b_qubits,num_int,num_dec)##d_a -->b
    ene_8_dg(qc_dist,0,1,var_qubits,a_qubits,8,num_q_for_res,num_int,num_dec)## A-->a
    #####
    
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
with open('3r_3c_5i10d_r1_e.70.txt', 'w') as file:
    file.write(str(data))


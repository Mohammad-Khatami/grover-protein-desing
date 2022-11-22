from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library.standard_gates import UGate
from qiskit.circuit.library.standard_gates import *
from qiskit.quantum_info import Statevector

###################

def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "Diff"
    return U_s
#A new quantum ripple-carry addition circuit
def add(qc_s,a_qubits,b_qubits,o_qubits,m):
    for i in range (1,m):
        qc_s.cx(a_qubits[i],b_qubits[i])
    qc_s.cx(a_qubits[1],o_qubits)
    for i in range (2,m):
        qc_s.cx(a_qubits[i],a_qubits[i-1])
    qc_s.ccx(a_qubits[0],b_qubits[0],o_qubits[0])
    qc_s.ccx(o_qubits[0],b_qubits[1],a_qubits[1])
    for i in range (2,m-1):
        qc_s.ccx(a_qubits[i-1],b_qubits[i],a_qubits[i])
    for i in range (1,m-1):
        qc_s.x(b_qubits[i])
    qc_s.cx(o_qubits,b_qubits[1])
    for i in range (1,m-1):
        qc_s.cx(a_qubits[i],b_qubits[i+1])
    i=m-2
    for k in range (2,m-1):
        qc_s.ccx(a_qubits[i-1],b_qubits[i],a_qubits[i])
        i=i-1
    qc_s.ccx(o_qubits[0],b_qubits[1],a_qubits[1])
    qc_s.ccx(a_qubits[0],b_qubits[0],o_qubits[0])
    for i in range (1,m-1):
        qc_s.x(b_qubits[i])
    i=m-1
    for k in range (2,m):
        qc_s.cx(a_qubits[i],a_qubits[i-1])
        i=i-1
    qc_s.cx(a_qubits[1],o_qubits)
    for i in range (0,m):
        qc_s.cx(a_qubits[i],b_qubits[i])

def add_dg(qc_s,a_qubits,b_qubits,o_qubits,m):
    i=m-1
    for k in range (0,m):
        qc_s.cx(a_qubits[i],b_qubits[i])
        i=i-1
    qc_s.cx(a_qubits[1],o_qubits)
    for i in range (2,m):
        qc_s.cx(a_qubits[i],a_qubits[i-1])
    i=m-2
    for k in range (1,m-1):
        qc_s.x(b_qubits[i])
        i=i-1
    qc_s.ccx(a_qubits[0],b_qubits[0],o_qubits[0])
    qc_s.ccx(o_qubits[0],b_qubits[1],a_qubits[1])
    for i in range (2,m-1):
        qc_s.ccx(a_qubits[i-1],b_qubits[i],a_qubits[i])
    i=m-2
    for k in range (1,m-1):
        qc_s.cx(a_qubits[i],b_qubits[i+1])
        i=i-1
    qc_s.cx(o_qubits,b_qubits[1])
    i=m-2
    for k in range (1,m-1):
        qc_s.x(b_qubits[i])
        i=i-1
    i=m-2
    for k in range (2,m-1):
        qc_s.ccx(a_qubits[i-1],b_qubits[i],a_qubits[i])
        i=i-1
    qc_s.ccx(o_qubits[0],b_qubits[1],a_qubits[1])
    qc_s.ccx(a_qubits[0],b_qubits[0],o_qubits[0])
    i=m-1
    for k in range (2,m):
        qc_s.cx(a_qubits[i],a_qubits[i-1])
        i=i-1
    qc_s.cx(a_qubits[1],o_qubits)
    i=m-1
    for k in range (1,m):
        qc_s.cx(a_qubits[i],b_qubits[i])
        i=i-1

def energy(qc,a,d,x,y,var_qubits,ene_a_qubits):
    a=a*3
    b=a+1
    c=a+2
    d=3*d
    e=d+1
    f=d+2
    qc.barrier()
#################################  H1-H1 000 000 -> -3
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
#################################  H1-H2 000 001 -> -1
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
#################################  H1-Pol1 000 010 -> +1
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
#################################  H1-Pos 000 100 -> +2
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
#################################  H1-neg 000 101 -> +2
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
#################################  H2-H2 001 001 -> -2
    qc.barrier()
    qc.barrier()
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(x+1,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
#################################  H2-pol2 001 011 -> +1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[f])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[f])
#################################  H2-pos 001 100 -> +1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f):
        qc.x(var_qubits[i])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f):
        qc.x(var_qubits[i])
#################################  H2-neg 001 101 -> +1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
#################################  pol1-pol1 010 010 -> -3
    qc.barrier()
    qc.barrier()
    qc.barrier()

    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])

    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])

    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
#################################  pol1-pol2 010 011 -> -2
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[f])
    for i in range(x+1,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[f])
#################################  pol1-pos 010 100 -> -1
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
#################################  pol1-neg 010 101 -> -1
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[e])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[e])
#################################  pol2-pol2 011 011 -> -3
    qc.barrier()
    qc.barrier()
    qc.barrier()
    qc.x(var_qubits[c])
    qc.x(var_qubits[f])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])

    qc.x(var_qubits[c])
    qc.x(var_qubits[f])

#################################  pol2-pos 011 100 -> +1
    qc.barrier()
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])

#################################  pos-pos 100 100 -> +4
    qc.barrier()
    qc.barrier()
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+2])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
#################################  pos-neg 100 101 -> -4
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
#################################  neg-neg 101 101 -> +3
    qc.barrier()
    qc.barrier()
    qc.barrier()
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
#################################  X1-X1 110 110 -> -1
    qc.barrier()
    qc.barrier()
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[d])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[d])

#################################  H1-H2 001 000 -> -1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
#################################  H1-Pol1 010 000 -> +1
    qc.barrier()
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
#################################  H1-Pos 100 000 -> +2
    qc.barrier()
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
#################################  H1-neg 101 000 -> +2
    qc.barrier()
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
#################################  H2-pol2 011 001 -> +1
    qc.barrier()
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[c])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[c])
#################################  H2-pos 100 001 -> +1
    qc.barrier()
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(a,c):
        qc.x(var_qubits[i])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(a,c):
        qc.x(var_qubits[i])
#################################  H2-neg 101 001 -> +1
    qc.barrier()
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
#################################  pol1-pol2 011 010 -> -2
    qc.barrier()
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
    for i in range(x+1,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
#################################  pol1-pos 100 010 -> -1
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
#################################  pol1-neg 101 010 -> -1
    qc.barrier()
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
#################################  pol2-pos 100 011 -> +1
    qc.barrier()
    qc.x(var_qubits[f])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    qc.x(var_qubits[f])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
#################################  pos-neg 101 100 -> -4
    qc.barrier()
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.x(var_qubits[b])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.x(var_qubits[b])

def energy_dg(qc,a,d,x,y,var_qubits,ene_a_qubits):
    a=a*3
    b=a+1
    c=a+2
    d=3*d
    e=d+1
    f=d+2
    qc.barrier()
#################################  H1-H1 000 000 -> -3
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
#################################  H1-H2 000 001 -> -1
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
#################################  H1-Pol1 000 010 -> +1
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
#################################  H1-Pos 000 100 -> +2
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
#################################  H1-neg 000 101 -> +2
    qc.barrier()
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(a,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
#################################  H2-H2 001 001 -> -2
    qc.barrier()
    qc.barrier()
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(x+1,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
#################################  H2-pol2 001 011 -> +1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[f])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[f])
#################################  H2-pos 001 100 -> +1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f):
        qc.x(var_qubits[i])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f):
        qc.x(var_qubits[i])
#################################  H2-neg 001 101 -> +1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[e])
#################################  pol1-pol1 010 010 -> -3
    qc.barrier()
    qc.barrier()
    qc.barrier()
    
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
#################################  pol1-pol2 010 011 -> -2
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[f])
    for i in range(x+1,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[f])
#################################  pol1-pos 010 100 -> -1
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
#################################  pol1-neg 010 101 -> -1
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[e])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.x(var_qubits[e])
#################################  pol2-pol2 011 011 -> -3
    qc.barrier()
    qc.barrier()
    qc.barrier()
    qc.x(var_qubits[c])
    qc.x(var_qubits[f])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])

    qc.x(var_qubits[c])
    qc.x(var_qubits[f])

#################################  pol2-pos 011 100 -> +1
    qc.barrier()
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    qc.x(var_qubits[c])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])

#################################  pos-pos 100 100 -> +4
    qc.barrier()
    qc.barrier()
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+2])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
#################################  pos-neg 100 101 -> -4
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
#################################  neg-neg 101 101 -> +3
    qc.barrier()
    qc.barrier()
    qc.barrier()
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    qc.x(var_qubits[b])
    qc.x(var_qubits[e])
#################################  X1-X1 110 110 -> -1
    qc.barrier()
    qc.barrier()
    qc.barrier()  
    qc.x(var_qubits[a])
    qc.x(var_qubits[d])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[d])

#################################  H1-H2 001 000 -> -1
    qc.barrier()
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    for i in range(b,c+1):
        qc.x(var_qubits[i])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
#################################  H1-Pol1 010 000 -> +1
    qc.barrier()
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[c])
#################################  H1-Pos 100 000 -> +2
    qc.barrier()
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
#################################  H1-neg 101 000 -> +2
    qc.barrier()
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x+1])
    for i in range(d,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
#################################  H2-pol2 011 001 -> +1
    qc.barrier()
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[c])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[c])
#################################  H2-pos 100 001 -> +1
    qc.barrier()
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(a,c):
        qc.x(var_qubits[i])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    for i in range(a,c):
        qc.x(var_qubits[i])
#################################  H2-neg 101 001 -> +1
    qc.barrier()
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    for i in range(e,f+1):
        qc.x(var_qubits[i])
    qc.x(var_qubits[b])
#################################  pol1-pol2 011 010 -> -2
    qc.barrier()
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
    for i in range(x+1,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
#################################  pol1-pos 100 010 -> -1
    qc.barrier()
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
#################################  pol1-neg 101 010 -> -1
    qc.barrier()
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
    for i in range(x,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[f])
    qc.x(var_qubits[b])
#################################  pol2-pos 100 011 -> +1
    qc.barrier()
    qc.x(var_qubits[f])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
    qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[x])
    qc.x(var_qubits[f])
    qc.x(var_qubits[a])
    qc.x(var_qubits[b])
#################################  pos-neg 101 100 -> -4
    qc.barrier()
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.x(var_qubits[b])
    for i in range(x+2,y):#for HH
        qc.mct([var_qubits[a],var_qubits[b],var_qubits[c],var_qubits[d]
                ,var_qubits[e],var_qubits[f]],ene_a_qubits[i])
    qc.x(var_qubits[d])
    qc.x(var_qubits[e])
    qc.x(var_qubits[b])



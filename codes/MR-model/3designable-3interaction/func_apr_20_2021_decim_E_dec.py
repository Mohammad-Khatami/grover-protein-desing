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

def binnary_list(number,num_int,num_dec):
    c_list=[]
    if number>=0: # for posittive and 0 numbers!
        #a for decimal parts
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
        a_bin.reverse()
        #b for the int numbers
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2 
        c_list=a_bin+b_bin
       # return (a_bin,b_bin)
    if (number<0) and ((number%1)!=0):# for negative containing decimal
        number=-number
        #a for decimal parts
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
            a_bin[i]=1-a_bin[i]
        a_bin.reverse()
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2
            b_bin[i]=1-b_bin[i]
        c_list=a_bin+b_bin
        c_list.reverse()
        for i in range (num_int):
            b_bin[i]=c_list[i]
        y=0
        for i in range (num_int,num_int+num_dec):
            a_bin[y]=c_list[i]
            y=y+1
        y=0
        w=1
        for i in reversed (range (num_int+num_dec)):
            c_list[i]=c_list[i]+w
            if c_list[i]==0:
                c_list[i]=0
                w=0
            if c_list[i]==1:
                c_list[i]=1
                w=0
            if c_list[i]==2:
                c_list[i]=0
                w=1
        for i in range (num_int):
            b_bin[i]=c_list[i]
        y=0
        for i in range (num_int,num_int+num_dec):
            a_bin[y]=c_list[i]
            y=y+1
        y=0
        a_bin.reverse()
        b_bin.reverse()
        c_list=a_bin+b_bin

#$#
#    if (number<0) and ((number%1)!=0):# for negative containing decimal
#        number=-number
#        a=number%1
#        a=1-a
#        a_bin=[]
#        for i in range(num_dec):
#            a=a*2
#            if a < 1:
#                x=0
#            else:
#                x=1
#                a=a-1
#            a_bin.append(x)
#        a_bin.reverse()
#        #b for the int numbers
#        b=int(number//1)
#        b_bin=[]
#        for i in range (num_int):
#            x=b%2
#            b_bin.append(x)
#            b=b//2 
#        for i in range (num_int):
#            b_bin[i]=1-b_bin[i]
#        c_list=a_bin+b_bin
#$#
    if (number<0) and ((number%1)==0):# for negative without decimal
        number=-number
        number=number-1
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
        a_bin.reverse()
        #b for the int numbers
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2 
        for i in range (num_int):
            b_bin[i]=1-b_bin[i]
        c_list=a_bin+b_bin
       # return (a_bin,b_bin)
    return c_list

def binnary_res(number,num_int):
    b=int(number//1)
    b_bin=[]
    for i in range (num_int):
        x=b%2
        b_bin.append(x)
        b=b//2
   # return (a_bin,b_bin)
    return (b_bin)

def ene_16(qc_w,res_a,res_b,var_qubits,ene_a_qubits,ene_n,num_q_for_res,num_int,num_dec):
    aa=res_a*num_q_for_res
    ab=aa+1
    ac=aa+2
    ad=aa+3
    
    ba=res_b*num_q_for_res
    bb=ba+1
    bc=ba+2
    bd=ba+3

    p=ene_n
#    energy_list_up=[-1,1,0,2,2,0,0,0,1,1,1,0,0,
#                -8,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -10,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -3,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -6,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -8,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -10,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -3,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -6,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -6,-1,-1,0,0,1,0,0,0,-4,0]
#    energy_list_diag=[-3,-2,-3,-3,+4,+3,-1,0,
#                  -3,-2,-3,-3,+4,+3,-1,0]
    energy_list_up=[-1.3,1.1,0.59,2.45,2.5,0,0,0,1,1.325,
                1.5,0,0,-2,-1,-1,0,0,1.5,0,0,0,-4.3,
                0.5,0,0,0,0,-1.3,1.1,0.59,2.45,2.5,0,0,
                0,1,1.325,1.5,0,0,-2,-1,-1,0,0,1.5,0,-2.1,
                0,0,-4.3,0.5,0,0,0,0,-1.3,1.1,0.59,1.1,
                2.45,2.5,0,0,0,1,1.325,-1.3,1.1,0.59,2.45,2.5,0,
                1.5,0,0,-2,-1,-1,0,0,1.5,0,0,0,-4.3,
                0.5,0,0,0,0,-1.3,1.1,0.59,2.45,2.5,0,0,
                0,1,1.325,1.5,0,0,-2,-1,-1,0,0,1.5,0,
                0,0,-4.3,0.5,0,0,0,0]
    energy_list_diag=[-3.2,-2.1,-3,-3.6,+4,+3,-1.6,0.5,
                  -3.33,-2.5,-3.45,-3,+4,+3.9,-1,0]
#######################
    t=0
    for j in range (ene_n):
        res2=binnary_res(j,num_q_for_res)
        for i in range (j+1, ene_n):
            res1=binnary_res(i,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            #print(energy_list_up[t])
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ad],
                        var_qubits[ba],var_qubits[bb],var_qubits[bc],var_qubits[bd]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1
#######################
    t=0
    for i in range (p):
        res=binnary_res(i,num_q_for_res)
        lis=binnary_list(energy_list_diag[i],num_int,num_dec)
        qc_w.barrier()
            #print (res1)
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
        for k in range(num_int+num_dec):
            if lis[k]==1:
                qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ad],
                        var_qubits[ba],var_qubits[bb],var_qubits[bc],var_qubits[bd]],ene_a_qubits[k])
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
#######################
    t=0
    for i in range (ene_n):
        res1=binnary_res(i,num_q_for_res)
        for j in range(i+1,ene_n):
            res2=binnary_res(j,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ad],
                        var_qubits[ba],var_qubits[bb],var_qubits[bc],var_qubits[bd]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1
def ene_16_dg(qc_w,res_a,res_b,var_qubits,ene_a_qubits,ene_n,num_q_for_res,num_int,num_dec):
    aa=res_a*num_q_for_res
    ab=aa+1
    ac=aa+2
    ad=aa+3
    
    ba=res_b*num_q_for_res
    bb=ba+1
    bc=ba+2
    bd=ba+3

    p=ene_n
#    energy_list_up=[-1,1,0,2,2,0,0,0,1,1,1,0,0,
#                -8,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -10,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -3,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -6,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -8,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -10,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -3,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -6,-1,-1,0,0,1,0,0,0,-4,0,0,
#                -6,-1,-1,0,0,1,0,0,0,-4,0]
#    energy_list_diag=[-3,-2,-3,-3,+4,+3,-1,0,
#                  -3,-2,-3,-3,+4,+3,-1,0]
    energy_list_up=[-1.3,1.1,0.59,2.45,2.5,0,0,0,1,1.325,
                1.5,0,0,-2,-1,-1,0,0,1.5,0,0,0,-4.3,
                0.5,0,0,0,0,-1.3,1.1,0.59,2.45,2.5,0,0,
                0,1,1.325,1.5,0,0,-2,-1,-1,0,0,1.5,0,-2.1,
                0,0,-4.3,0.5,0,0,0,0,-1.3,1.1,0.59,1.1,
                2.45,2.5,0,0,0,1,1.325,-1.3,1.1,0.59,2.45,2.5,0,
                1.5,0,0,-2,-1,-1,0,0,1.5,0,0,0,-4.3,
                0.5,0,0,0,0,-1.3,1.1,0.59,2.45,2.5,0,0,
                0,1,1.325,1.5,0,0,-2,-1,-1,0,0,1.5,0,
                0,0,-4.3,0.5,0,0,0,0]
    energy_list_diag=[-3.2,-2.1,-3,-3.6,+4,+3,-1.6,0.5,
                  -3.33,-2.5,-3.45,-3,+4,+3.9,-1,0]

#######################
    t=0
    for j in range (ene_n):
        res2=binnary_res(j,num_q_for_res)
        for i in range (j+1, ene_n):
            res1=binnary_res(i,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            #print(energy_list_up[t])
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ad],
                        var_qubits[ba],var_qubits[bb],var_qubits[bc],var_qubits[bd]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1
#######################
    t=0
    for i in range (p):
        res=binnary_res(i,num_q_for_res)
        lis=binnary_list(energy_list_diag[i],num_int,num_dec)
        qc_w.barrier()
            #print (res1)
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
        for k in range(num_int+num_dec):
            if lis[k]==1:
                qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ad],
                        var_qubits[ba],var_qubits[bb],var_qubits[bc],var_qubits[bd]],ene_a_qubits[k])
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
#######################
    t=0
    for i in range (ene_n):
        res1=binnary_res(i,num_q_for_res)
        for j in range(i+1,ene_n):
            res2=binnary_res(j,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ad],
                        var_qubits[ba],var_qubits[bb],var_qubits[bc],var_qubits[bd]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1



def ene_8(qc_w,res_a,res_b,var_qubits,ene_a_qubits,ene_n,num_q_for_res,num_int,num_dec):
    aa=res_a*num_q_for_res
    ab=aa+1
    ac=aa+2
#    ad=aa+3
    
    ba=res_b*num_q_for_res
    bb=ba+1
    bc=ba+2
#    bd=ba+3

    p=ene_n
#    energy_list_up=[-1,1,0,2,2,0,0,0,1,1,1,0,0,
#                   -2,-1,-1,0,0,1,0,0,0,-4,0,0,
#                    0,0,0]
#    energy_list_diag=[-3,-2,-3,-3,+4,+3,-1,0]
#    energy_list_up=[-1.1,1.25,0.3,2.3,2.122,0.4,-0.04,0.8,1.3,1.1,1.2,0.4,0.1,
#                   -2.3,-1.2,-1.7,0.7,0.54,1.55,0.63,0.56,0.12,-4.43,0.55,0.92,
#                    0.16,0.77,0.34]
#    energy_list_diag=[-3.39,-2.26,-3.87,-3.89,+4.1,+3.4,-1.5,0.5]
#
    energy_list_up=[-1.3,1.1,0.59,2.45,2.5,0,0,0,1,1.325,1.5,0,0,
                   -2,-1,-1,0,0,1.5,0,0,0,-4.3,0.5,0,
                    0,0,0]
    energy_list_diag=[-3.2,-2.2,-3.7,-3.51,+4.2,+3.3,-1.5,0.1]
#######################
    t=0
    for j in range (ene_n):
        res2=binnary_res(j,num_q_for_res)
        for i in range (j+1, ene_n):
            res1=binnary_res(i,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            #print(energy_list_up[t])
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ba]
                        ,var_qubits[bb],var_qubits[bc]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1
#######################
    t=0
    for i in range (p):
        res=binnary_res(i,num_q_for_res)
        lis=binnary_list(energy_list_diag[i],num_int,num_dec)
        qc_w.barrier()
            #print (res1)
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
        for k in range(num_int+num_dec):
            if lis[k]==1:
                qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ba]
                        ,var_qubits[bb],var_qubits[bc]],ene_a_qubits[k])
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
#######################
    t=0
    for i in range (ene_n):
        res1=binnary_res(i,num_q_for_res)
        for j in range(i+1,ene_n):
            res2=binnary_res(j,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ba]
                        ,var_qubits[bb],var_qubits[bc]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1
def ene_8_dg(qc_w,res_a,res_b,var_qubits,ene_a_qubits,ene_n,num_q_for_res,num_int,num_dec):
    aa=res_a*num_q_for_res
    ab=aa+1
    ac=aa+2
#    ad=aa+3
    
    ba=res_b*num_q_for_res
    bb=ba+1
    bc=ba+2
#    bd=ba+3

    p=ene_n
#    energy_list_up=[-1,1,0,2,2,0,0,0,1,1,1,0,0,
#                   -2,-1,-1,0,0,1,0,0,0,-4,0,0,
#                   0,0,0]
#    energy_list_diag=[-3,-2,-3,-3,+4,+3,-1,0]
#    energy_list_up=[-1.1,1.25,0.3,2.3,2.122,0.4,-0.04,0.8,1.3,1.1,1.2,0.4,0.1,
#                   -2.3,-1.2,-1.7,0.7,0.54,1.55,0.63,0.56,0.12,-4.43,0.55,0.92,
#                    0.16,0.77,0.34]
#    energy_list_diag=[-3.39,-2.26,-3.87,-3.89,+4.1,+3.4,-1.5,0.5]

    energy_list_up=[-1.3,1.1,0.59,2.45,2.5,0,0,0,1,1.325,1.5,0,0,
                   -2,-1,-1,0,0,1.5,0,0,0,-4.3,0.5,0,
                    0,0,0]
    energy_list_diag=[-3.2,-2.2,-3.7,-3.51,+4.2,+3.3,-1.5,0.1]
#######################
    t=0
    for j in range (ene_n):
        res2=binnary_res(j,num_q_for_res)
        for i in range (j+1, ene_n):
            res1=binnary_res(i,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            #print(energy_list_up[t])
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ba]
                        ,var_qubits[bb],var_qubits[bc]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1
#######################
    t=0
    for i in range (p):
        res=binnary_res(i,num_q_for_res)
        lis=binnary_list(energy_list_diag[i],num_int,num_dec)
        qc_w.barrier()
            #print (res1)
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
        for k in range(num_int+num_dec):
            if lis[k]==1:
                qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ba]
                        ,var_qubits[bb],var_qubits[bc]],ene_a_qubits[k])
        for w in range(num_q_for_res):
            if (res[w]==0) and (energy_list_diag[i]!=0):
                qc_w.x(var_qubits[w+aa])
                qc_w.x(var_qubits[w+ba])
#######################
    t=0
    for i in range (ene_n):
        res1=binnary_res(i,num_q_for_res)
        for j in range(i+1,ene_n):
            res2=binnary_res(j,num_q_for_res)
            lis=binnary_list(energy_list_up[t],num_int,num_dec)
            qc_w.barrier()
            #print (res1)
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            for k in range(num_int+num_dec):
                if lis[k]==1:
                    qc_w.mct([var_qubits[aa],var_qubits[ab],var_qubits[ac],var_qubits[ba]
                        ,var_qubits[bb],var_qubits[bc]],ene_a_qubits[k])
            for w in range(num_q_for_res):
                if (res1[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+aa])
                if (res2[w]==0) and (energy_list_up[t]!=0):
                    qc_w.x(var_qubits[w+ba])
            t=t+1






def multiply(qc,a_qubits,b_qubits,mp_qubits,mp_res_qubits,o_qubits,m):
    t=0
    for t in range (m):
        for i in range (m):
            qc.ccx(a_qubits[i],b_qubits[t],mp_qubits[i+t])
        qc.barrier()        
        add(qc,mp_qubits,mp_res_qubits,o_qubits,2*m)
        for i in range (m):
            qc.ccx(a_qubits[i],b_qubits[t],mp_qubits[i+t])
        qc.barrier()
def multiply_dg(qc,a_qubits,b_qubits,mp_qubits,mp_res_qubits,o_qubits,m):
    t=0
    for t in range (m):
        for i in range (m):
            qc.ccx(a_qubits[i],b_qubits[t],mp_qubits[i+t])
        qc.barrier()        
        add(qc,mp_qubits,mp_res_qubits,o_qubits,2*m)
        for i in range (m):
            qc.ccx(a_qubits[i],b_qubits[t],mp_qubits[i+t])
        qc.barrier()


def multiply_same(qc_b,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec):
#c is the out put
#a and b are the inputs
# rest will be zero!
    for i in range(num_int+num_dec):
        qc_b.cx(a_qubits[i],a_ext_qubits[i])
        qc_b.cx(b_qubits[i],b_ext_qubits[i])
    for j in range(num_int+num_dec):
        qc_b.cx(a_qubits[num_int+num_dec-1],a_ext_qubits[j+num_int+num_dec])
        qc_b.cx(b_qubits[num_int+num_dec-1],b_ext_qubits[j+num_int+num_dec])
#         print (num_int+num_dec-1,j+num_int+num_dec)
        
    t=0
    for t in range (2*(num_int+num_dec)):
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
        add(qc_b,mp_qubits,mp_res_qubits,o_qubits,2*(num_int+num_dec))
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
    j=0
    for j in range (int(num_int+num_dec)):
        qc_b.cx(mp_res_qubits[j+num_dec],c_qubits[j])
  ########################################## 
    t=0
    for t in range (2*(num_int+num_dec)):
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
        add_dg(qc_b,mp_qubits,mp_res_qubits,o_qubits,2*(num_int+num_dec))
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
    for j in range(num_int+num_dec):
        qc_b.cx(a_qubits[num_int+num_dec-1],a_ext_qubits[j+num_int+num_dec])
        qc_b.cx(b_qubits[num_int+num_dec-1],b_ext_qubits[j+num_int+num_dec])
    for i in range(num_int+num_dec):
        qc_b.cx(a_qubits[i],a_ext_qubits[i])
        qc_b.cx(b_qubits[i],b_ext_qubits[i])

def multiply_same_dg(qc_b,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,
                      a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec):

    for i in range(num_int+num_dec):
        qc_b.cx(a_qubits[i],a_ext_qubits[i])
        qc_b.cx(b_qubits[i],b_ext_qubits[i])
    for j in range(num_int+num_dec):
        qc_b.cx(a_qubits[num_int+num_dec-1],a_ext_qubits[j+num_int+num_dec])
        qc_b.cx(b_qubits[num_int+num_dec-1],b_ext_qubits[j+num_int+num_dec])
#         print (num_int+num_dec-1,j+num_int+num_dec)
        
    t=0
    for t in range (2*(num_int+num_dec)):
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
        add(qc_b,mp_qubits,mp_res_qubits,o_qubits,2*(num_int+num_dec))
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
    j=0
    for j in range (int(num_int+num_dec)):
        qc_b.cx(mp_res_qubits[j+num_dec],c_qubits[j])
  ########################################## 
    t=0
    for t in range (2*(num_int+num_dec)):
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
        add_dg(qc_b,mp_qubits,mp_res_qubits,o_qubits,2*(num_int+num_dec))
        for i in range (2*(num_int+num_dec)):
            qc_b.ccx(a_ext_qubits[i],b_ext_qubits[t],mp_qubits[i+t])
        qc_b.barrier()
    for j in range(num_int+num_dec):
        qc_b.cx(a_qubits[num_int+num_dec-1],a_ext_qubits[j+num_int+num_dec])
        qc_b.cx(b_qubits[num_int+num_dec-1],b_ext_qubits[j+num_int+num_dec])
    for i in range(num_int+num_dec):
        qc_b.cx(a_qubits[i],a_ext_qubits[i])
        qc_b.cx(b_qubits[i],b_ext_qubits[i])

def neg(qc_s,m,w_qubits,x_qubits,o_qubits):
    qc_s.x(w_qubits)
    qc_s.x(x_qubits[0])
    add(qc_s,w_qubits,x_qubits,o_qubits,m)
    qc_s.x(w_qubits)

def neg_dg(qc_s,m,w_qubits,x_qubits,o_qubits):
    qc_s.x(w_qubits)
    add_dg(qc_s,w_qubits,x_qubits,o_qubits,m)
    qc_s.x(x_qubits[0])    
    qc_s.x(w_qubits)

def cp(qc,m,a_qubits,b_qubits):#copy a on b --- re do the cp to cancel it!!
    for i in range(m):
        qc.cx(a_qubits[i],b_qubits[i])
        
def cp_dg(qc,m,a_qubits,b_qubits):#copy a on b --- re do the cp to cancel it!!
    for i in range(m):
        qc.cx(a_qubits[i],b_qubits[i])

def binnary(qc,number,a_qubits,num_int,num_dec):
    c_list=[]
    if number>=0: # for posittive and 0 numbers!
        #a for decimal parts
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
        a_bin.reverse()
        #b for the int numbers
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2
        c_list=a_bin+b_bin
       # return (a_bin,b_bin)

    if (number<0) and ((number%1)!=0):# for negative containing decimal
        number=-number
        #a for decimal parts
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
            a_bin[i]=1-a_bin[i]
        a_bin.reverse()
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2
            b_bin[i]=1-b_bin[i]
        c_list=a_bin+b_bin
        c_list.reverse()
        for i in range (num_int):
            b_bin[i]=c_list[i]
        y=0
        for i in range (num_int,num_int+num_dec):
            a_bin[y]=c_list[i]
            y=y+1
        y=0
        w=1
        for i in reversed (range (num_int+num_dec)):
            c_list[i]=c_list[i]+w
            if c_list[i]==0:
                c_list[i]=0
                w=0
            if c_list[i]==1:
                c_list[i]=1
                w=0
            if c_list[i]==2:
                c_list[i]=0
                w=1
        for i in range (num_int):
            b_bin[i]=c_list[i]
        y=0
        for i in range (num_int,num_int+num_dec):
            a_bin[y]=c_list[i]
            y=y+1
        y=0
        a_bin.reverse()
        b_bin.reverse()


    if (number<0) and ((number%1)==0):# for negative without decimal
        number=-number
        number=number-1
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
        a_bin.reverse()
        #b for the int numbers
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2
        for i in range (num_int):
            b_bin[i]=1-b_bin[i]
        c_list=a_bin+b_bin
       # return (a_bin,b_bin)
    for i in range (num_dec):
        if a_bin[i]==1:
            qc.x(a_qubits[i])
    for i in range (num_int):
        if b_bin[i]==1:
            qc.x(a_qubits[i+num_dec])

def binnary_dg(qc,number,a_qubits,num_int,num_dec):
    c_list=[]
    if number>=0: # for posittive and 0 numbers!
        #a for decimal parts
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
        a_bin.reverse()
        #b for the int numbers
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2
        c_list=a_bin+b_bin
       # return (a_bin,b_bin)

    if (number<0) and ((number%1)!=0):# for negative containing decimal
        number=-number
        #a for decimal parts
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
            a_bin[i]=1-a_bin[i]
        a_bin.reverse()
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2
            b_bin[i]=1-b_bin[i]
        c_list=a_bin+b_bin
        c_list.reverse()
        for i in range (num_int):
            b_bin[i]=c_list[i]
        y=0
        for i in range (num_int,num_int+num_dec):
            a_bin[y]=c_list[i]
            y=y+1
        y=0
        w=1
        for i in reversed (range (num_int+num_dec)):
            c_list[i]=c_list[i]+w
            if c_list[i]==0:
                c_list[i]=0
                w=0
            if c_list[i]==1:
                c_list[i]=1
                w=0
            if c_list[i]==2:
                c_list[i]=0
                w=1
        for i in range (num_int):
            b_bin[i]=c_list[i]
        y=0
        for i in range (num_int,num_int+num_dec):
            a_bin[y]=c_list[i]
            y=y+1
        y=0
        a_bin.reverse()
        b_bin.reverse()


    if (number<0) and ((number%1)==0):# for negative without decimal
        number=-number
        number=number-1
        a=number%1
        a_bin=[]
        for i in range(num_dec):
            a=a*2
            if a < 1:
                x=0
            else:
                x=1
                a=a-1
            a_bin.append(x)
        a_bin.reverse()
        #b for the int numbers
        b=int(number//1)
        b_bin=[]
        for i in range (num_int):
            x=b%2
            b_bin.append(x)
            b=b//2
        for i in range (num_int):
            b_bin[i]=1-b_bin[i]
        c_list=a_bin+b_bin
       # return (a_bin,b_bin)
    for i in range (num_dec):
        if a_bin[i]==1:
            qc.x(a_qubits[i])
    for i in range (num_int):
        if b_bin[i]==1:
            qc.x(a_qubits[i+num_dec])









def decimal(result,m,n): #converts the first keys in the results to decimal!
    res = list(result.keys())[0]
    t=[int(d) for d in str(res)]
    t[m+n-1]=1
    res_dec=0.00
    num=0.00
    for i in range (m+n):
        num=t[i]*(2.0**(m-1-i))
        res_dec+=num
    return(res_dec)





def find_dist (xa,xb,ya,yb,za,zb,qc_pow,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,rx_qubits,ry_qubits,rz_qubits,num_int,num_dec):
#def find_dist (xa,xb,ya,yb,za,zb,d_th,qc_pow,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,o_qubits,rx_qubits,ry_qubits,rz_qubits,num_int,num_dec):
    m=num_int+num_dec
    binnary(qc_pow,xa,a_qubits,num_int,num_dec)
    add(qc_pow,a_qubits,rx_qubits,o_qubits,m)
    binnary_dg(qc_pow,xa,a_qubits,num_int,num_dec)
    ###a(x)-b(x)
    xb=-xb
    binnary(qc_pow,xb,a_qubits,num_int,num_dec)
    add(qc_pow,a_qubits,rx_qubits,o_qubits,m)
    binnary_dg(qc_pow,xb,a_qubits,num_int,num_dec)
    #########
    binnary(qc_pow,ya,a_qubits,num_int,num_dec)
    add(qc_pow,a_qubits,ry_qubits,o_qubits,m)
    binnary_dg(qc_pow,ya,a_qubits,num_int,num_dec)
    ###a(y)-b(y)
    yb=-yb
    binnary(qc_pow,yb,a_qubits,num_int,num_dec)
    add(qc_pow,a_qubits,ry_qubits,o_qubits,m)
    binnary_dg(qc_pow,yb,a_qubits,num_int,num_dec)
    #########
    binnary(qc_pow,za,a_qubits,num_int,num_dec)
    add(qc_pow,a_qubits,rz_qubits,o_qubits,m)
    binnary_dg(qc_pow,za,a_qubits,num_int,num_dec)
    ###a(z)-b(z)
    zb=-zb
    binnary(qc_pow,zb,a_qubits,num_int,num_dec)
    add(qc_pow,a_qubits,rz_qubits,o_qubits,m)
    binnary_dg(qc_pow,zb,a_qubits,num_int,num_dec)
        ##~~~~~~~~##
    cp(qc_pow,m,rx_qubits,a_qubits)
    multiply_same(qc_pow,rx_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add(qc_pow,b_qubits,c_qubits,o_qubits,m)
    multiply_same_dg(qc_pow,rx_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    cp_dg(qc_pow,m,rx_qubits,a_qubits)
        ##~~~~~~~~##
    cp(qc_pow,m,ry_qubits,a_qubits)
    multiply_same(qc_pow,ry_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add(qc_pow,b_qubits,c_qubits,o_qubits,m)
    multiply_same_dg(qc_pow,ry_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    cp_dg(qc_pow,m,ry_qubits,a_qubits)
        ##~~~~~~~~##
    cp(qc_pow,m,rz_qubits,a_qubits)
    multiply_same(qc_pow,rz_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add(qc_pow,b_qubits,c_qubits,o_qubits,m)
    multiply_same_dg(qc_pow,rz_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    cp_dg(qc_pow,m,rz_qubits,a_qubits)

######### for d_th
#    ###r^2 - d_th^2
#    d_th=-d_th
#    binnary(qc_pow,d_th,a_qubits,num_int,num_dec)
#    add(qc_pow,a_qubits,c_qubits,o_qubits,m)
#    binnary_dg(qc_pow,d_th,a_qubits,num_int,num_dec)
############

def find_dist_dg (xa,xb,ya,yb,za,zb,qc_pow,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,rx_qubits,ry_qubits,rz_qubits,num_int,num_dec):
    m=num_int+num_dec
######## for d_th
#    d_th=-d_th
#    binnary(qc_pow,d_th,a_qubits,num_int,num_dec)
#    add_dg(qc_pow,a_qubits,c_qubits,o_qubits,m)
#    binnary_dg(qc_pow,d_th,a_qubits,num_int,num_dec)
########

    cp(qc_pow,m,rz_qubits,a_qubits)
    multiply_same(qc_pow,rz_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add_dg(qc_pow,b_qubits,c_qubits,o_qubits,m)
    multiply_same_dg(qc_pow,rz_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    cp_dg(qc_pow,m,rz_qubits,a_qubits)

    cp(qc_pow,m,ry_qubits,a_qubits)
    multiply_same(qc_pow,ry_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add_dg(qc_pow,b_qubits,c_qubits,o_qubits,m)
    multiply_same_dg(qc_pow,ry_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    cp_dg(qc_pow,m,ry_qubits,a_qubits)

    cp(qc_pow,m,rx_qubits,a_qubits)
    multiply_same(qc_pow,rx_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    add_dg(qc_pow,b_qubits,c_qubits,o_qubits,m)
    multiply_same_dg(qc_pow,rx_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)
    cp_dg(qc_pow,m,rx_qubits,a_qubits)
        ##~~~~~~~~##

    zb=-zb
    binnary(qc_pow,zb,a_qubits,num_int,num_dec)
    add_dg(qc_pow,a_qubits,rz_qubits,o_qubits,m)
    binnary_dg(qc_pow,zb,a_qubits,num_int,num_dec)
    binnary(qc_pow,za,a_qubits,num_int,num_dec)
    add_dg(qc_pow,a_qubits,rz_qubits,o_qubits,m)
    binnary_dg(qc_pow,za,a_qubits,num_int,num_dec)
    yb=-yb
    binnary(qc_pow,yb,a_qubits,num_int,num_dec)
    add_dg(qc_pow,a_qubits,ry_qubits,o_qubits,m)
    binnary_dg(qc_pow,yb,a_qubits,num_int,num_dec)
    binnary(qc_pow,ya,a_qubits,num_int,num_dec)
    add_dg(qc_pow,a_qubits,ry_qubits,o_qubits,m)
    binnary_dg(qc_pow,ya,a_qubits,num_int,num_dec)
    xb=-xb
    binnary(qc_pow,xb,a_qubits,num_int,num_dec)
    add_dg(qc_pow,a_qubits,rx_qubits,o_qubits,m)
    binnary_dg(qc_pow,xb,a_qubits,num_int,num_dec)
    binnary(qc_pow,xa,a_qubits,num_int,num_dec)
    add_dg(qc_pow,a_qubits,rx_qubits,o_qubits,m)
    binnary_dg(qc_pow,xa,a_qubits,num_int,num_dec)


def x_0(qc_s,num_int,num_dec,a_qubits,b_qubits,o_qubits):
    m=num_int+num_dec
    v=num_dec-num_int+1
    ##########
    qc_s.cx(a_qubits[m-1],b_qubits[v])
    qc_s.cx(a_qubits[m-1],o_qubits)
    qc_s.barrier()

    u=0
    for i in range(num_int-1):
        qc_s.x(o_qubits)
        qc_s.ccx(a_qubits[m-u-2],o_qubits,b_qubits[v+i+1])
        qc_s.x(o_qubits)
        qc_s.cx(b_qubits[v+i+1],o_qubits)
        qc_s.barrier()
        u=u+1

    qc_s.x(b_qubits[v:num_dec+1])
    qc_s.mct(b_qubits[v:num_dec+1],o_qubits)
    qc_s.x(b_qubits[v:num_dec+1])
    qc_s.barrier()
    qc_s.x(o_qubits)
    v=0
    qc_s.barrier()


def x_0_dg(qc_s,num_int,num_dec,a_qubits,b_qubits,o_qubits):
    m=num_int+num_dec
    v=num_dec-num_int+1
    ##########
    qc_s.x(o_qubits)
    qc_s.barrier()
    qc_s.x(b_qubits[v:num_dec+1])
    qc_s.mct(b_qubits[v:num_dec+1],o_qubits)
    qc_s.x(b_qubits[v:num_dec+1])
    qc_s.barrier()

    u=num_int-2
    for i in reversed(range(num_int-1)):
        qc_s.cx(b_qubits[v+i+1],o_qubits)
        qc_s.x(o_qubits)
        qc_s.ccx(a_qubits[m-u-2],o_qubits,b_qubits[v+i+1])
        qc_s.x(o_qubits)

        qc_s.barrier()
        u=u-1

    qc_s.cx(a_qubits[m-1],o_qubits)
    qc_s.cx(a_qubits[m-1],b_qubits[v])
    v=0


def inv_s3(qc_s,w_qubits,a_qubits,b_qubits,c_qubits,d_qubits,e_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec):
# note w has the number!
# a-->x_1, b--> 0, C-->> 0, e-->> X_2,  d-->> result!
    m=num_int+num_dec
    x_0(qc_s,num_int,num_dec,w_qubits,a_qubits,o_qubits) # a has the x_0 
    # calculate X_1
    ########w*X_i-1
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    neg(qc_s,m,c_qubits,d_qubits,o_qubits) # d -->> -(w * X_i-1 ^2)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0 --> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0-->b
    ###
    binnary(qc_s,2,b_qubits,num_int,num_dec)#b-->2
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)## C-->> 2 *X_i-1
    add(qc_s,c_qubits,d_qubits,o_qubits,m) # d has x_1
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)## C-->> 0
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    x_0_dg(qc_s,num_int,num_dec,w_qubits,a_qubits,o_qubits) # a -->0 , b--> 0, C-->> 0, d-->> X_1 
    cp(qc_s,m,d_qubits,a_qubits)
    cp(qc_s,m,a_qubits,d_qubits) #a -->x_1 , b--> 0, C-->> 0, d-->> 0
    # calculate X_2 
    ########w*X_i-1
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### w*X_i-1-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    neg(qc_s,m,c_qubits,d_qubits,o_qubits) # d -->> -(w * X_i-1 ^2)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0--> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### 0-->b
    ###
    binnary(qc_s,2,b_qubits,num_int,num_dec)#b-->2
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 2 *X_i-1
    add(qc_s,c_qubits,d_qubits,o_qubits,m) # d has x_1
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    cp(qc_s,m,d_qubits,e_qubits)
    ##########
    binnary(qc_s,2,b_qubits,num_int,num_dec)
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    add_dg(qc_s,c_qubits,d_qubits,o_qubits,m)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### w*X_i-1-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    neg_dg(qc_s,m,c_qubits,d_qubits,o_qubits)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0--> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### 0-->b
    ### a-->x_1, b--> 0, C-->> 0, d-->> 0, e-->> X_2
    # calculate X_3
    ########w*X_i-1
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### w*X_i-1-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    neg(qc_s,m,c_qubits,d_qubits,o_qubits) # d -->> -(w * X_i-1 ^2)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0--> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### 0-->b
    ##
    binnary(qc_s,2,b_qubits,num_int,num_dec)#b-->2
    multiply_same(qc_s,e_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    add(qc_s,c_qubits,d_qubits,o_qubits,m) # d has x_3
    multiply_same_dg(qc_s,e_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    return(d_qubits)



def inv_s3_dg(qc_s,w_qubits,a_qubits,b_qubits,c_qubits,d_qubits,e_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec):
# note w has the number!
# a-->x_1, b--> 0, C-->> 0, e-->> X_2,  d-->> result!
    m=num_int+num_dec
    binnary(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    multiply_same(qc_s,e_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    add_dg(qc_s,c_qubits,d_qubits,o_qubits,m) # d has x_3
    multiply_same_dg(qc_s,e_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)#b-->2
    ##
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### 0-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0--> c
    neg_dg(qc_s,m,c_qubits,d_qubits,o_qubits) # d -->> -(w * X_i-1 ^2)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### w*X_i-1-->b
    ########w*X_i-1
    # calculate X_3
    ### a-->x_1, b--> 0, C-->> 0, d-->> 0, e-->> X_2
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### 0-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0--> c
    neg(qc_s,m,c_qubits,d_qubits,o_qubits)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### w*X_i-1-->b
    binnary(qc_s,2,b_qubits,num_int,num_dec)
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    add(qc_s,c_qubits,d_qubits,o_qubits,m)
    binnary(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)
    ##########
    cp_dg(qc_s,m,d_qubits,e_qubits)
    binnary(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 0
    add_dg(qc_s,c_qubits,d_qubits,o_qubits,m) # d has x_1
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# ## C-->> 2 *X_i-1
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)#b-->2
    ###
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### 0-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0--> c
    neg_dg(qc_s,m,c_qubits,d_qubits,o_qubits) # d -->> -(w * X_i-1 ^2)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)### w*X_i-1-->b
    ########w*X_i-1
    # calculate X_2
    cp_dg(qc_s,m,a_qubits,d_qubits) #a -->x_1 , b--> 0, C-->> 0, d-->> 0
    cp_dg(qc_s,m,d_qubits,a_qubits)
    x_0(qc_s,num_int,num_dec,w_qubits,a_qubits,o_qubits) # a -->0 , b--> 0, C-->> 0, d-->> X_1
    binnary(qc_s,2,b_qubits,num_int,num_dec)# a-->x_0, b--> 0, C-->> 0, d-->> X_1
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)## C-->> 0
    add_dg(qc_s,c_qubits,d_qubits,o_qubits,m) # d has x_1
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)## C-->> 2 *X_i-1
    binnary_dg(qc_s,2,b_qubits,num_int,num_dec)#b-->2
    ###
    multiply_same(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0-->b
    multiply_same(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# 0 --> c
    neg_dg(qc_s,m,c_qubits,d_qubits,o_qubits) # d -->> -(w * X_i-1 ^2)
    multiply_same_dg(qc_s,a_qubits,b_qubits,c_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1*X_i-1 --> c
    multiply_same_dg(qc_s,w_qubits,a_qubits,b_qubits,mp_qubits,mp_res_qubits,a_ext_qubits,b_ext_qubits,o_qubits,num_int,num_dec)# w*X_i-1-->b
    ########w*X_i-1
    # calculate X_1
    x_0_dg(qc_s,num_int,num_dec,w_qubits,a_qubits,o_qubits) # a has the x_0


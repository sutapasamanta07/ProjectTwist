#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 11:34:36 2022

@author: sutapa
"""

import matplotlib.pyplot as plt
from qiskit import *
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, transpile, Aer
from qiskit.tools.visualization import plot_histogram
from qiskit.providers.ibmq.managed import IBMQJobManager
from qiskit.circuit import Parameter
#from qiskit.circuit.library.standard_gates import U3Gate
from qiskit.quantum_info import Statevector
import numpy as np
from numpy import *
import math
#IBMQ.save_account('61f3d8f001320c577b3f4ee176a8504dbe5c8951a9397725fc7d2d843fab8f5d381d6259ef6377903e43eb7f14fbaf40faba0885b0abba6cb760adf58d6228e9', overwrite=True)
#IBMQ.delete_account()
#print(IBMQ.active_account())
#IBMQ.save_account('ea8636dddfe30737d43c4028f41dcfef14e672200543c4fa4e550c04c19b9fdb2059dea90eae79933487fffeed5a1a27b370308fdbf3f1f7e0ebfa6e58512592', overwrite=True)#pouyan
IBMQ.save_account('557bf66a69d4906a509feaff4379ff3959627f143c76716b09605d9d0578df9fdd3e47105316f1f30ad7957e2a7c60a35b194f311a20c62d9673ac87f5208a49', overwrite=True)#Armin


IBMQ.load_account()
#provider=IBMQ.get_provider(hub='ibm-q')
#provider=IBMQ.get_provider(hub='ibm-q-research-2')
provider=IBMQ.get_provider(hub='ibm-q-bnl')
#print(provider.backends())
#simulator=provider.get_backend('ibmq_kolkata')
#simulator=provider.get_backend('ibmq_mumbai')
#simulator=provider.get_backend('ibmq_guadalupe')
#simulator = provider.get_backend('ibm_auckland')
#simulator = provider.get_backend('ibmq_manila')
#simulator = provider.get_backend('ibmq_lima')
simulator = provider.get_backend('ibmq_montreal')
#simulator=provider.get_backend('ibmq_qasm_simulator')
#simulator=provider.get_backend('simulator_statevector')
#simulator = Aer.get_backend('qasm_simulator')
job_manager = IBMQJobManager()


N_repeat =20 # N_repeat: number of repeats per circuit
Nq=4
N_events = pow(2,Nq)
circuit_list=[]

qasm_str= """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
cx q[0], q[1];
rz(0.21991148575128555) q[1];
cx q[0], q[1];
cx q[1], q[2];
rz(0.21991148575128555) q[2];
cx q[1], q[2];
cx q[3], q[1];
rz(0.21991148575128555) q[1];
cx q[3], q[1]; 
h q[3];
cx q[2], q[3];
rz(0.21991148575128555) q[3];
cx q[2],q[3];
h q[3];
rx(2.199114857512855) q[0];
rx(2.199114857512855) q[1];
rx(2.199114857512855) q[2];

"""
for t in range(1,N_repeat+1):
    qf,cf=QuantumRegister(Nq), ClassicalRegister(Nq)
    circ=QuantumCircuit(qf)
    #change input to Y-basis
    circ.rx(1.5707963267948966,0)
    circ.rx(1.5707963267948966,1)
    circ.rx(1.5707963267948966,2)
    circ.rx(1.5707963267948966,3)
    circ.barrier(qf)
    #load U
    uni=QuantumCircuit.from_qasm_str(qasm_str).repeat(t)
    circ.append(uni,qf)

    qc = circ
    qc.barrier(qf)
    qc.rx(1.5707963267948966,0)
    qc.rx(1.5707963267948966,1)
    qc.rx(1.5707963267948966,2)
    qc.rx(1.5707963267948966,3)
    qc.add_register(cf)
    qc.measure(qf,cf)
    
    circuit_list.append(qc)
    

#qc.draw(output='mpl')



circuit_list = transpile(circuit_list, backend=simulator,initial_layout=[9,8,11,14],optimization_level=3)
job_set= job_manager.run(circuit_list, backend=simulator,shots=8192)
#print(job_set.jobs())
results = job_set.results()
#print(results.get_counts(0))
#print(results.get_counts(1))
#print(results.get_counts(2))
#print(results.get_counts(3))


states=['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']

Q0val=[]
Q1val=[]
Q2val=[]
Q3val=[]

for t in range(0,N_repeat):
    prob=[]
    counts = results.get_counts(t)
    for i in range(0,16):
        if(counts.get(states[i])==None):
            bit_count=0
        else:
            bit_count=counts.get(states[i])
        prob.append(bit_count/8192)
    
    Q3p=0
    Q3m=0
    Q2p=0
    Q2m=0
    Q1p=0
    Q1m=0
    Q0p=0
    Q0m=0
    for i in range(0,8):
          Q3p+= prob[i]
          Q3m+= prob[8+i]
    Q3 = Q3p-Q3m
    Q3val.append(Q3)

    for i in range(0,4):
        Q2p+=prob[i]+prob[8+i]
        Q2m+=prob[4+i]+prob[12+i]
    Q2 = Q2p-Q2m
    Q2val.append(Q2)
    
    for i in range(0,2):
        Q1p+=prob[i]+prob[4+i]+prob[8+i]+prob[12+i]
        Q1m+=prob[2+i]+prob[6+i]+prob[10+i]+prob[14+i]
    Q1 = Q1p-Q1m
    Q1val.append(Q1)

    for i in range(0,8):
        Q0p+=prob[2*i]
        Q0m+=prob[2*i+1]
    Q0=Q0p-Q0m
    Q0val.append(Q0)
    
myfile=open("Q4PeriodicExpt.txt",'w')
myfile.write("Q0=")
print(Q0val,file=myfile)
   
    
myfile.write("Q1=")
print(Q1val,file=myfile)
    
myfile.write("Q2=")
print(Q2val,file=myfile)

myfile.write("Q3=")
print(Q3val,file=myfile)
    
myfile.close()

plt.plot(Q0val,'-s',label='q0 ')
plt.plot(Q1val,'-s',label='q1 ')
plt.plot(Q2val,'-s',label='q2 ')
plt.plot(Q3val,'-s',label='q3 ')

plt.ylabel('$<s_y>$')
plt.xlabel('t')

#plt.show()
plt.savefig('Q4PeriodicExpt.pdf')

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
from qiskit.quantum_info import SparsePauliOp
#from qiskit.circuit.library.standard_gates import U3Gate
from qiskit.quantum_info import Statevector
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator,Sampler, Options
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
#simulator = "ibmq_kolkata"
#simulator = "ibmq_mumbai"
simulator = "ibm_hanoi"
#simulator = "ibm_cairo"
#simulator = "ibmq_guadalupe"
#simulator = "ibm_auckland"
#simulator = "ibmq_manila"
#simulator = "ibmq_lima"
#simulator = "ibmq_montreal"
#simulator = "ibmq_qasm_simulator"
job_manager = IBMQJobManager()


N_repeat =21 # N_repeat: number of repeats per circuit
Nq=12
N_events = pow(2,Nq)
circuit_list=[]

qasm_str= """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[12];
cx q[0], q[1];
rz(0.21991148575128555) q[1];
cx q[0], q[1];
cx q[1], q[2];
rz(0.21991148575128555) q[2];
cx q[1], q[2];
cx q[2], q[3];
rz(0.21991148575128555) q[3];
cx q[2], q[3];
cx q[3], q[4];
rz(0.21991148575128555) q[4];
cx q[3], q[4];
cx q[4], q[5];
rz(0.21991148575128555) q[5];
cx q[4], q[5];
cx q[5], q[6];
rz(0.21991148575128555) q[6];
cx q[5], q[6];
cx q[6], q[7];
rz(0.21991148575128555) q[7];
cx q[6], q[7];
cx q[7], q[8];
rz(0.21991148575128555) q[8];
cx q[7], q[8];
cx q[8], q[9];
rz(0.21991148575128555) q[9];
cx q[8], q[9];
cx q[9], q[10];
rz(0.21991148575128555) q[10];
cx q[9], q[10];
cx q[11], q[0];
rz(0.21991148575128555) q[0];
cx q[11], q[0];
h q[11];
cx q[10], q[11];
rz(0.21991148575128555) q[11];
cx q[10],q[11];
h q[11];
rx(2.199114857512855) q[0];
rx(2.199114857512855) q[1];
rx(2.199114857512855) q[2];
rx(2.199114857512855) q[3];
rx(2.199114857512855) q[4];
rx(2.199114857512855) q[5];
rx(2.199114857512855) q[6];
rx(2.199114857512855) q[7];
rx(2.199114857512855) q[8];
rx(2.199114857512855) q[9];
rx(2.199114857512855) q[10];
"""
for t in range(0,N_repeat):
    qf,cf=QuantumRegister(Nq), ClassicalRegister(Nq)
    circ=QuantumCircuit(qf)
    #change input to Y-basis 1111
    #circ.x(0)
    #circ.x(1)
    #circ.x(2)
    #circ.x(3)
    circ.rx(1.5707963267948966,0)
    circ.rx(1.5707963267948966,1)
    circ.rx(1.5707963267948966,2)
    circ.rx(1.5707963267948966,3)
    circ.rx(1.5707963267948966,4)
    circ.rx(1.5707963267948966,5)
    circ.rx(1.5707963267948966,6)
    circ.rx(1.5707963267948966,7)
    circ.rx(1.5707963267948966,8)
    circ.rx(1.5707963267948966,9)
    circ.rx(1.5707963267948966,10)
    circ.rx(1.5707963267948966,11)
    circ.barrier(qf)
    #load U
    uni=QuantumCircuit.from_qasm_str(qasm_str).repeat(t)
    circ.append(uni,qf)

    qc = circ
    #qc.barrier(qf)
    #qc.rx(1.5707963267948966,0)
    #qc.rx(1.5707963267948966,1)
    #qc.rx(1.5707963267948966,2)
    #qc.rx(1.5707963267948966,3)
    #qc.add_register(cf)
    #qc.measure(qf,cf)
    
    circuit_list.append(qc)
    

#qc.draw(output='mpl')
#circuit_list = transpile(circuit_list, backend=simulator,initial_layout=[8,11,14,16])
service = QiskitRuntimeService()
options = Options()
options.execution.shots = 8192
options.resilience_level = 0
options.optimization_level = 3
options.transpilation.initial_layout = [12,15,18,21,23,24,25,22,19,16,14,13]
obs0 = SparsePauliOp("IIIIIIIIIIIY")
obs1 = SparsePauliOp("IIIIIIIIIIYI")
obs2 = SparsePauliOp("IIIIIIIIIYII")
obs3 = SparsePauliOp("YIIIIIIIIIII")
obs_list0 = [obs0]*len(circuit_list)
obs_list1 = [obs1]*len(circuit_list)
obs_list2 = [obs2]*len(circuit_list)
obs_list3 = [obs3]*len(circuit_list)

with Session(service=service, backend=simulator) as session:
    estimator = Estimator(session=session, options=options)
    job0 = estimator.run(circuits=circuit_list,observables=obs_list0)
    job1 = estimator.run(circuits=circuit_list,observables=obs_list1)
    job2 = estimator.run(circuits=circuit_list,observables=obs_list2)
    job3 = estimator.run(circuits=circuit_list,observables=obs_list3)
    #sampler =Sampler(session=session, options=options)
    #job_set = sampler.run(circuits=circuit_list)
    #results = job_set.result()
    q0val = job0.result().values
    q1val = job1.result().values
    q2val = job2.result().values
    q3val = job3.result().values
    #print(q3val)



    
myfile=open("Q12ErrorCorrectionRL0Hanoi.txt",'w')
myfile.write("Q0=")
print(q0val,file=myfile)
   
    
myfile.write("Q1=")
print(q1val,file=myfile)
    
myfile.write("Q2=")
print(q2val,file=myfile)

myfile.write("Q11=")
print(q3val,file=myfile)
    
myfile.close()

plt.plot(q0val,'-o',label='q0 ')
plt.plot(q1val,'-o',label='q1 ')
plt.plot(q2val,'-o',label='q2 ')
plt.plot(q3val,'-o',label='q11 ')
plt.title("Error Mitigation RL=0, Initial state=[111111111111]_y, Device = IBM Hanoi")
plt.ylabel('$<s_y>$')
plt.xlabel('t')
plt.legend()
# #plt.show()
plt.savefig('Q12ErrorCorrectionRL0Hanoi.pdf')

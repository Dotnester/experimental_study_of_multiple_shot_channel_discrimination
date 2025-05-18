from qiskit import QuantumCircuit
import numpy as np

"""
This file contains circuits for the channel discrimination experiment on the IBMQ.
"""
class ExperimentCircuits:

    def __init__(self, n_qubits:int):
        self.n_qubits = n_qubits
        self.qc = QuantumCircuit(n_qubits)

    def set_rz_for_perfect_disc(self):
        qc = self.qc
        n_qubits = self.n_qubits
        qc.rz(np.pi/n_qubits, range(n_qubits))
        self.qc = qc
    
    def set_simple_premeas_rot_mtx(self, measure:bool):
        qc = self.qc
        n_qubits = self.n_qubits
        qc.barrier()
        if n_qubits == 1:
            qc.sx(0)
        else:
            qc.ecr(0,1)
            qc.sx(range(n_qubits))
        if measure:
            qc.measure_all()
        self.qc = qc

    def set_disc(self):
        qc = self.qc
        n_qubits = self.n_qubits

        qc.sx(range(n_qubits))
        
        if n_qubits == 2:
            qc.ecr(0,1)
        
        elif n_qubits == 3:
            qc.ecr(1,0)
            qc.ecr(1,2)
            qc.x(0)
        
        elif n_qubits == 4:
            qc.ecr(1,2)
            qc.ecr(2,3)
            qc.ecr(1,0)

        elif n_qubits == 5:
            qc.ecr(1,2)
            qc.ecr(1,0)
            qc.ecr(2,3)
            qc.ecr(3,4)
            qc.x([0,1,2])

        elif n_qubits == 6:
            qc.ecr(2,3)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(3,4)
            qc.ecr(4,5)
            qc.x([2,3])

        elif n_qubits == 7:
            qc.ecr(2,3)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(3,4)
            qc.ecr(4,5)
            qc.ecr(5,6)
            qc.x([0,1,4])

        elif n_qubits == 8:
            qc.ecr(3,4)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(4,5)
            qc.ecr(5,6)
            qc.ecr(6,7)
            qc.x([2,5])

        elif n_qubits == 9:
            qc.ecr(3,4)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(4,5)
            qc.ecr(5,6)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.x([0,1,3,4,6])

        elif n_qubits == 10:
            qc.ecr(4,5)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(5,6)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.x([2,4,5,7])

        elif n_qubits == 11:
            qc.ecr(4,5)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(5,6)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.x([0,1,3,6,8])

        elif n_qubits == 12:
            qc.ecr(5,6)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)
            qc.x([2,4,7,9])
        
        elif n_qubits == 13:
            qc.ecr(5,6)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)
            qc.ecr(11,12)
            qc.x([2,4,7,9,11,12]) 
        
        elif n_qubits == 14:
            qc.ecr(6,7)
            qc.ecr(6,5)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)
            qc.ecr(11,12)
            qc.ecr(12,13)
            qc.x([2,4,6,7,9,11])
        
        elif n_qubits == 15:
            qc.ecr(6,7)
            qc.ecr(6,5)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)
            qc.ecr(11,12)
            qc.ecr(12,13)
            qc.ecr(13,14)
            qc.x([0,1,3,5,8,10,12])
        qc.barrier()
        self.qc = qc

    def set_XOR_premeas_rot_mtx(self, measure:bool = True):
        qc = self.qc
        n_qubits = self.n_qubits
        qc.barrier()
        if n_qubits == 1:
            qc.sx(0)
            
        elif n_qubits == 2:
            qc.ecr(0,1)
            qc.sx(0)
            qc.ecr(0,1)
            qc.x([0,1])
        
        elif n_qubits == 3:
            qc.ecr(1,2)
            qc.ecr(1,0)
            qc.sx(1)
            qc.ecr(1,0)
            qc.ecr(1,2)
        
        elif n_qubits == 4:
            
            qc.ecr(2,3)
            qc.ecr(1,0)
            qc.ecr(1,2)
            qc.sx([1])
            qc.ecr(1,2)
            qc.ecr(1,0)
            qc.ecr(2,3)

        elif n_qubits == 5:
            qc.ecr(3,4)
            qc.ecr(2,3)
            qc.ecr(1,0)
            qc.ecr(1,2)
            qc.sx(1)
            qc.ecr(1,2)
            qc.ecr(1,0)
            qc.ecr(2,3)
            qc.ecr(3,4)
        
        elif n_qubits == 6:
            qc.ecr(4,5)
            qc.ecr(3,4)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(2,3)
            qc.sx(2)
            qc.ecr(2,3)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(3,4)
            qc.ecr(4,5)
        
        elif n_qubits == 7:
            qc.ecr(5,6)
            qc.ecr(4,5)
            qc.ecr(3,4)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(2,3)
            qc.sx(2)
            qc.ecr(2,3)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(3,4)
            qc.ecr(4,5)
            qc.ecr(5,6)

        elif n_qubits == 8:
            qc.ecr(6,7)
            qc.ecr(5,6)
            qc.ecr(4,5)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(3,4)
            qc.sx(3)
            qc.ecr(3,4)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(4,5)
            qc.ecr(5,6)
            qc.ecr(6,7)
        
        elif n_qubits == 9:
            qc.ecr(7,8)
            qc.ecr(6,7)
            qc.ecr(5,6)
            qc.ecr(4,5)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(3,4)
            qc.sx(3)
            qc.ecr(3,4)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(4,5)
            qc.ecr(5,6)
            qc.ecr(6,7)
            qc.ecr(7,8)

        elif n_qubits == 10:
            qc.ecr(8,9)
            qc.ecr(7,8)
            qc.ecr(6,7)
            qc.ecr(5,6)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(4,3)
            qc.ecr(4,5)
            qc.sx(4)
            qc.ecr(4,5)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(5,6)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)

        elif n_qubits == 11:
            qc.ecr(9,10)
            qc.ecr(8,9)
            qc.ecr(7,8)
            qc.ecr(6,7)
            qc.ecr(5,6)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(4,3)
            qc.ecr(4,5)
            qc.sx(4)
            qc.ecr(4,5)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(5,6)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)

        elif n_qubits == 12:
            qc.ecr(10,11)
            qc.ecr(9,10)
            qc.ecr(8,9)
            qc.ecr(7,8)
            qc.ecr(6,7)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(4,3)
            qc.ecr(5,4)
            qc.ecr(5,6)
            qc.sx(5)
            qc.ecr(5,6)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)

        elif n_qubits == 13:
            qc.ecr(11,12)
            qc.ecr(10,11)
            qc.ecr(9,10)
            qc.ecr(8,9)
            qc.ecr(7,8)
            qc.ecr(6,7)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(4,3)
            qc.ecr(5,4)
            qc.ecr(5,6)
            qc.sx(5)
            qc.ecr(5,6)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(6,7)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)
            qc.ecr(11,12)

        elif n_qubits == 14:
            qc.ecr(12,13)
            qc.ecr(11,12)
            qc.ecr(10,11)
            qc.ecr(9,10)
            qc.ecr(8,9)
            qc.ecr(7,8)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(4,3)
            qc.ecr(5,4)
            qc.ecr(6,5)
            qc.ecr(6,7)
            qc.sx(6)
            qc.ecr(6,7)
            qc.ecr(6,5)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)
            qc.ecr(11,12)
            qc.ecr(12,13)

        if n_qubits == 15:
            qc.ecr(13,14)
            qc.ecr(12,13)
            qc.ecr(11,12)
            qc.ecr(10,11)
            qc.ecr(9,10)
            qc.ecr(8,9)
            qc.ecr(7,8)
            qc.ecr(1,0)
            qc.ecr(2,1)
            qc.ecr(3,2)
            qc.ecr(4,3)
            qc.ecr(5,4)
            qc.ecr(6,5)
            qc.ecr(6,7)
            qc.sx(6)
            qc.ecr(6,7)
            qc.ecr(6,5)
            qc.ecr(5,4)
            qc.ecr(4,3)
            qc.ecr(3,2)
            qc.ecr(2,1)
            qc.ecr(1,0)
            qc.ecr(7,8)
            qc.ecr(8,9)
            qc.ecr(9,10)
            qc.ecr(10,11)
            qc.ecr(11,12)
            qc.ecr(12,13)
            qc.ecr(13,14)
        if measure:
            qc.measure_all()

        self.qc = qc
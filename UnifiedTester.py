from __future__ import annotations

import os
import json
from typing import List, Dict
import re
from copy import deepcopy

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.providers import BackendV2
from qiskit_ibm_runtime import SamplerV2
from qiskit_aer import AerSimulator


class TesterResultStorage:
    def __init__(self, names: List[str], simulated_counts: List[Dict[str, int]], real_counts: List[Dict[str, int]]) -> None:
        '''
        Assumes name format Q<n_qubits>_L<m_layers>_{RZ,IDENT}_{SHORT,XOR}
        '''
        self.names = names
        self.simulated_counts = simulated_counts
        self.real_counts = real_counts
        self.processed_results = None

    def copy(self) -> TesterResultStorage:
        return TesterResultStorage(
            deepcopy(self.names),
            deepcopy(self.simulated_counts),
            deepcopy(self.real_counts)
        )

    def save_to_directory(self, directory: str):
        os.makedirs(directory, exist_ok=True)
        
        with open(os.path.join(directory, "names.json"), "w") as f:
            json.dump(self.names, f)
        
        with open(os.path.join(directory, "simulated_counts.json"), "w") as f:
            json.dump(self.simulated_counts, f)
        
        with open(os.path.join(directory, "real_counts.json"), "w") as f:
            json.dump(self.real_counts, f)

    @classmethod
    def load_from_directory(cls, directory: str):
        with open(os.path.join(directory, "names.json"), "r") as f:
            names = json.load(f)
        
        with open(os.path.join(directory, "simulated_counts.json"), "r") as f:
            simulated_counts = json.load(f)
        
        with open(os.path.join(directory, "real_counts.json"), "r") as f:
            real_counts = json.load(f)
        
        return cls(names, simulated_counts, real_counts)

    @classmethod
    def from_unified_tester(cls, tester:UnifiedTester):
        if tester.real_counts == None:
            assert "UnifiedTester has no real counts"
        
        return cls(tester.circuit_names, tester.sim_counts, tester.real_counts)

    @staticmethod
    def counts_within_xor_dist(counts: Dict[str,int], origin: str, dist: int) -> int:
        final = 0
        for bitstring, count in counts.items():
            hamming_distance = sum(bit1 != bit2 for bit1, bit2 in zip(bitstring, origin))
            if hamming_distance <= dist:
                final = final + count
        return final
    
    @staticmethod
    def counts_at_xor_dist(counts: Dict[str,int], origin: str, dist: int) -> int:
        final = 0
        for bitstring, count in counts.items():
            hamming_distance = sum(bit1 != bit2 for bit1, bit2 in zip(bitstring, origin))
            if hamming_distance == dist:
                final = final + count
        return final
    
    @staticmethod
    def hamming_distance_to_set(string_set: set[str], origin: str) -> int:
        final = len(origin)
        for bitstring in string_set:
            hamming_distance = sum(bit1 != bit2 for bit1, bit2 in zip(bitstring, origin))
            if hamming_distance < final:
                final = hamming_distance
        return final
    
    
    def process_results_xor(self):
        """
        Consider all ones as identity and zeros as rotation
        Corectly identifying RZ is true positive
        Corectly identifying I is true negative
        Correct results is RZ, but is identified as I is false negative
        Correct results is I, but is identified as RZ is false positive
        Also computes random guess towards either I or RZ which cant be determined (G prefix)
        """
        pattern = r'Q(\d+)_L(\d+)_.*' # reg exp pattern for n of qubits and layers extraction

        self.processed_results = {}
        
        for i,name in enumerate(self.names):
            q_num, l_num = re.match(pattern, name).groups()

            ident = f'Q{q_num}L{l_num}'

            self.processed_results[ident] = {}

        for i,name in enumerate(self.names):
            q_num, l_num = re.match(pattern, name).groups()
            
            ident = f'Q{q_num}L{l_num}'

            n_qubits = int(q_num)

            bin_clas_dict = self.processed_results[ident]

            if "TP" not in bin_clas_dict.keys():
                bin_clas_dict["TP"] = 0
            if "FN" not in bin_clas_dict.keys():
                bin_clas_dict["FN"] = 0
            if "TN" not in bin_clas_dict.keys():
                bin_clas_dict["TN"] = 0
            if "FP" not in bin_clas_dict.keys():
                bin_clas_dict["FP"] = 0
            
            if "RZ" in name:
                bin_clas_dict["TP"] = self.counts_within_xor_dist(self.real_counts[i], "0"*n_qubits, (n_qubits-1)//2)
                bin_clas_dict["FN"] = self.counts_within_xor_dist(self.real_counts[i], "1"*n_qubits, (n_qubits-1)//2)
            if "IDENT" in name:
                bin_clas_dict["TN"] = self.counts_within_xor_dist(self.real_counts[i], "1"*n_qubits, (n_qubits-1)//2)
                bin_clas_dict["FP"] = self.counts_within_xor_dist(self.real_counts[i], "0"*n_qubits, (n_qubits-1)//2)  
            
            if "GTP" not in bin_clas_dict.keys():
                bin_clas_dict["GTP"] = 0
            if "GFN" not in bin_clas_dict.keys():
                bin_clas_dict["GFN"] = 0
            if "GTN" not in bin_clas_dict.keys():
                bin_clas_dict["GTN"] = 0
            if "GFP" not in bin_clas_dict.keys():
                bin_clas_dict["GFP"] = 0

            if n_qubits % 2 == 0:
                # random guess for strings with same nuber of zeros and ones
                counts_to_guess = self.counts_at_xor_dist(self.real_counts[i], "0"*n_qubits, n_qubits//2)
                if "RZ" in name:
                    bin_clas_dict["GTP"] = counts_to_guess // 2
                    bin_clas_dict["GFN"] = counts_to_guess - bin_clas_dict["GTP"]
                if "IDENT" in name:
                    bin_clas_dict["GTN"] = counts_to_guess // 2
                    bin_clas_dict["GFP"] = counts_to_guess - bin_clas_dict["GTN"]

            self.processed_results[ident] = bin_clas_dict


        return self.processed_results
    

    def process_results_short(self):
        """
        Corectly identifying RZ is true positive
        Corectly identifying I is true negative
        Correct results is RZ, but is identified as I is false negative
        Correct results is I, but is identified as RZ is false positive
        Also computes random guess towards either I or RZ which cant be determined (G prefix)
        """
        pattern = r'Q(\d+)_L(\d+)_.*' # reg exp pattern for n of qubits and layers extraction

        self.processed_results = {}
        rz_combinations = {}
        id_combinations = {}

        for i,name in enumerate(self.names):
            q_num, l_num = re.match(pattern, name).groups()

            circuit_idx = f'Q{q_num}L{l_num}'

            self.processed_results[circuit_idx] = {}
            rz_combinations[circuit_idx] = set()
            id_combinations[circuit_idx] = set()

        for i,name in enumerate(self.names):
            q_num, l_num = re.match(pattern, name).groups()

            circuit_idx = f'Q{q_num}L{l_num}'

            if "RZ" in name:
                rz_combinations[circuit_idx] = rz_combinations[circuit_idx].union(set(self.simulated_counts[i].keys()))

            if "IDENT" in name:
                id_combinations[circuit_idx] = id_combinations[circuit_idx].union(set(self.simulated_counts[i].keys()))

        for i,name in enumerate(self.names):
            q_num, l_num = re.match(pattern, name).groups()
            
            circuit_idx = f'Q{q_num}L{l_num}'

            bin_clas_dict = self.processed_results[circuit_idx]

            if "TP" not in bin_clas_dict.keys():
                bin_clas_dict["TP"] = 0
            if "FN" not in bin_clas_dict.keys():
                bin_clas_dict["FN"] = 0
            if "TN" not in bin_clas_dict.keys():
                bin_clas_dict["TN"] = 0
            if "FP" not in bin_clas_dict.keys():
                bin_clas_dict["FP"] = 0

            if "GTP" not in bin_clas_dict.keys():
                bin_clas_dict["GTP"] = 0
            if "GFN" not in bin_clas_dict.keys():
                bin_clas_dict["GFN"] = 0
            if "GTN" not in bin_clas_dict.keys():
                bin_clas_dict["GTN"] = 0
            if "GFP" not in bin_clas_dict.keys():
                bin_clas_dict["GFP"] = 0
            

            if "RZ" in name:
                counts_rz = 0
                counts_id = 0

                # random guess for strings that have same distance from both answears
                counts_to_guess = 0

                for key in self.real_counts[i]:
                    dist_to_rz = self.hamming_distance_to_set(rz_combinations[circuit_idx], key)
                    dist_to_id = self.hamming_distance_to_set(id_combinations[circuit_idx], key)

                    if dist_to_rz < dist_to_id:
                        counts_rz += self.real_counts[i][key] 
                    elif dist_to_rz > dist_to_id:
                        counts_id += self.real_counts[i][key]
                    else:
                        counts_to_guess += self.real_counts[i][key]

                bin_clas_dict["TP"] += counts_rz
                bin_clas_dict["FN"] += counts_id
                bin_clas_dict["GTP"] += counts_to_guess // 2
                bin_clas_dict["GFN"] += counts_to_guess - counts_to_guess // 2
            
            if "IDENT" in name:
                counts_rz = 0
                counts_id = 0

                # random guess for strings that have same distance from both answears
                counts_to_guess = 0

                for key in self.real_counts[i]:
                    dist_to_rz = self.hamming_distance_to_set(rz_combinations[circuit_idx], key)
                    dist_to_id = self.hamming_distance_to_set(id_combinations[circuit_idx], key)

                    if dist_to_rz < dist_to_id:
                        counts_rz += self.real_counts[i][key] 
                    elif dist_to_rz > dist_to_id:
                        counts_id += self.real_counts[i][key]
                    else:
                        counts_to_guess += self.real_counts[i][key]

                bin_clas_dict["TN"] += counts_id
                bin_clas_dict["FP"] += counts_rz
                bin_clas_dict["GTN"] = counts_to_guess // 2
                bin_clas_dict["GFP"] = counts_to_guess - counts_to_guess // 2


            self.processed_results[circuit_idx] = bin_clas_dict

        return self.processed_results


class UnifiedTester:
    def __init__(self, circuits:list[QuantumCircuit], backend:BackendV2, optimization_level:int, circuit_names:list[str] = [], sim_shots = 10000) -> None:
        '''
        elements of circuits and circuit_names should match one to one
        standard naming convection is Q<n_qubits>_L<m_layers>_{RZ,IDENT}_{SHORT,XOR}
        '''
        self.circuits = circuits
        self.circuit_names = circuit_names
        self.n_circ = len(self.circuits)
        self.pm = generate_preset_pass_manager(backend = backend, optimization_level=optimization_level)
        self.sampler = SamplerV2(backend)

        self.isa_circuits = self.pm.run(circuits)

        self.sim_counts = None
        self.sim_results(sim_shots)

        self.job = None
        self.real_counts = None

    def run_job(self, shots = 10000):
        if self.job != None:
            print("Cannot run multiple jobs per tester")
            return None

        self.job = self.sampler.run(self.isa_circuits, shots = shots) # bulk run
        print(f">>> Job ID: {self.job.job_id()}")

    def job_status(self):
        if self.job == None:
            print("Job doesn't exist (missing run_job?)")
            return None
        
        if not self.job.in_final_state():
            print("Job running")
            return None
        
        print("Job finnished")
 
    def collect_counts_from_job(self) -> list[dict[str, int]] | None:
        if self.real_counts != None:
            print("Counts already collected")
            return self.real_counts

        if self.job == None:
            print("Job doesn't exist (missing run_job?)")
            return None

        if not self.job.in_final_state():
            print("Cannot process running job")
            return None
        
        job_result = self.job.result()
        
        self.real_counts = []
        if hasattr(job_result[0], 'data'):
            for i in range(self.n_circ):
                self.real_counts.append(job_result[i].data.meas.get_counts())
        else:
            for i in range(self.n_circ):
                self.real_counts.append(job_result[i]["__value__"]["data"].meas.get_counts())

        return self.real_counts
    
    def collect_counts_from_ext_job(self, ext_job) -> list[dict[str, int]] | None:
        if ext_job == None:
            print("Provided job is None")
            return None
        
        job_result = ext_job.result()
        
        self.real_counts = []
        for i in range(self.n_circ):
            self.real_counts.append(job_result[i]["__value__"]["data"].meas.get_counts())

        return self.real_counts
        
    def sim_results(self,shots=100000) -> list[dict[str, int]]:
        if self.sim_counts != None:
            return self.sim_counts
        
        self.sim_counts = []

        simulator = AerSimulator()
        sim_sampler = SamplerV2(simulator)
        sim_job = sim_sampler.run(self.isa_circuits, shots = shots) # bulk run

        for i in range(self.n_circ):
            self.sim_counts.append(sim_job.result()[i].data.meas.get_counts())

        return self.sim_counts

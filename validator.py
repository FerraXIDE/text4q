from typing import List
from .core import QuantumCommand, GateType

class CommandValidator:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.measured_qubits = set()
        self.errors: List[str] = []
    
    def validate(self, command: QuantumCommand) -> bool:
        self.errors = []
        
        if command.gate == "CREATE":
            return True
        
        for qubit in command.qubits:
            if qubit >= self.num_qubits:
                self.errors.append(f"Qubit {qubit} fuera de rango")
                return False
        
        if command.gate == GateType.MEASURE:
            if command.qubits[0] in self.measured_qubits:
                self.errors.append(f"Qubit {command.qubits[0]} ya fue medido")
                return False
            self.measured_qubits.add(command.qubits[0])
        
        return True
    
    def get_errors(self) -> List[str]:
        return self.errors

from typing import Dict, Optional

class GateFactory:
    GATE_PROPS = {
        'H': {'num_qubits': 1, 'params': 0},
        'X': {'num_qubits': 1, 'params': 0},
        'Y': {'num_qubits': 1, 'params': 0},
        'Z': {'num_qubits': 1, 'params': 0},
        'S': {'num_qubits': 1, 'params': 0},
        'T': {'num_qubits': 1, 'params': 0},
        'CX': {'num_qubits': 2, 'params': 0},
        'CZ': {'num_qubits': 2, 'params': 0},
        'SWAP': {'num_qubits': 2, 'params': 0},
        'RX': {'num_qubits': 1, 'params': 1},
        'RY': {'num_qubits': 1, 'params': 1},
        'RZ': {'num_qubits': 1, 'params': 1},
    }
    
    @classmethod
    def list_gates(cls) -> list:
        return list(cls.GATE_PROPS.keys())

"""Quantum gates module for text4q"""

from enum import Enum
from typing import Dict, Optional

class GateType(Enum):
    """Supported types of quantum gates"""
    H = "H"
    X = "X"
    Y = "Y"
    Z = "Z"
    S = "S"
    T = "T"
    CX = "CX"
    CZ = "CZ"
    SWAP = "SWAP"
    RX = "RX"
    RY = "RY"
    RZ = "RZ"
    MEASURE = "MEASURE"
    BARRIER = "BARRIER"
    BLOCH = "BLOCH"


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

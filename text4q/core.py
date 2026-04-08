"""
text4q compiler core - Multi-idioma
"""
import re
from typing import List, Dict, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
    from qiskit.providers.basic_provider import BasicSimulator
    HAS_QISKIT = True
except ImportError:
    HAS_QISKIT = False
    print("Warning: Qiskit not installed. Install with: pip install qiskit")


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


@dataclass
class QuantumCommand:
    """It represents a single quantum command"""
    gate: Union[GateType, str]
    qubits: List[int]
    params: Optional[List[float]] = None
    cbits: Optional[List[int]] = None
    raw_text: str = ""
    
    def __post_init__(self):
        if isinstance(self.gate, str):
            try:
                self.gate = GateType[self.gate.upper()]
            except KeyError:
                pass


class Text4QCompiler:
    """
    Quantum Circuit Compiler - Multi-idioma
    
    Idiomas soportados:
    - Español: crear, medir, barrera
    - English: create, measure, barrier
    - Français: créer, mesurer, barrière
    - Português: criar, medir, barreira
    - Deutsch: erstelle, messen, barriere
    - 日本語 (Japonés): 作成, 測定, バリア
    - 中文 (Chino): 创建, 测量, 屏障
    """
    
    def __init__(self):
        self.commands: List[QuantumCommand] = []
        self.num_qubits: int = 0
        self.num_cbits: int = 0
        self.circuit: Optional['QuantumCircuit'] = None
        
        # Palabras clave en cada idioma
        create_words = ['crear', 'create', 'créer', 'criar', 'erstelle', '作成', '创建']
        measure_words = ['medir', 'measure', 'mesurer', 'medir', 'messen', '測定', '测量']
        barrier_words = ['barrera', 'barrier', 'barrière', 'barreira', 'barriere', 'バリア', '屏障']
        
        # Construir patrones dinámicamente
        create_pattern = r'^(' + '|'.join(create_words) + r')\s+(\d+)$'
        measure_pattern = r'^(' + '|'.join(measure_words) + r')\s+(\d+)(?:\s*->\s*(\d+))?$'
        barrier_pattern = r'^(' + '|'.join(barrier_words) + r')$'
        
        self.patterns = {
            'create': re.compile(create_pattern, re.IGNORECASE),
            'h': re.compile(r'^[hH]\s+(\d+)$'),
            'x': re.compile(r'^[xX]\s+(\d+)$'),
            'y': re.compile(r'^[yY]\s+(\d+)$'),
            'z': re.compile(r'^[zZ]\s+(\d+)$'),
            's': re.compile(r'^[sS]\s+(\d+)$'),
            't': re.compile(r'^[tT]\s+(\d+)$'),
            'cx': re.compile(r'^cx\s+(\d+)\s+(\d+)$', re.IGNORECASE),
            'cz': re.compile(r'^cz\s+(\d+)\s+(\d+)$', re.IGNORECASE),
            'swap': re.compile(r'^swap\s+(\d+)\s+(\d+)$', re.IGNORECASE),
            'rx': re.compile(r'^rx\(([^)]+)\)\s+(\d+)$', re.IGNORECASE),
            'ry': re.compile(r'^ry\(([^)]+)\)\s+(\d+)$', re.IGNORECASE),
            'rz': re.compile(r'^rz\(([^)]+)\)\s+(\d+)$', re.IGNORECASE),
            'measure': re.compile(measure_pattern, re.IGNORECASE),
            'barrier': re.compile(barrier_pattern, re.IGNORECASE),
            'bloch': re.compile(r'^bloch$', re.IGNORECASE),
        }
    
    def parse_command(self, text: str) -> Optional[QuantumCommand]:
        """Parse a text command into a QuantumCommand (multi-idioma)"""
        text = text.strip()
        
        match = self.patterns['create'].match(text)
        if match:
            num = int(match.group(2))
            return QuantumCommand(gate="CREATE", qubits=[], params=[num], raw_text=text)
        
        match = self.patterns['h'].match(text)
        if match:
            return QuantumCommand(gate=GateType.H, qubits=[int(match.group(1))], raw_text=text)
        
        match = self.patterns['x'].match(text)
        if match:
            return QuantumCommand(gate=GateType.X, qubits=[int(match.group(1))], raw_text=text)
        
        match = self.patterns['y'].match(text)
        if match:
            return QuantumCommand(gate=GateType.Y, qubits=[int(match.group(1))], raw_text=text)
        
        match = self.patterns['z'].match(text)
        if match:
            return QuantumCommand(gate=GateType.Z, qubits=[int(match.group(1))], raw_text=text)
        
        match = self.patterns['s'].match(text)
        if match:
            return QuantumCommand(gate=GateType.S, qubits=[int(match.group(1))], raw_text=text)
        
        match = self.patterns['t'].match(text)
        if match:
            return QuantumCommand(gate=GateType.T, qubits=[int(match.group(1))], raw_text=text)
        
        match = self.patterns['cx'].match(text)
        if match:
            return QuantumCommand(gate=GateType.CX, qubits=[int(match.group(1)), int(match.group(2))], raw_text=text)
        
        match = self.patterns['cz'].match(text)
        if match:
            return QuantumCommand(gate=GateType.CZ, qubits=[int(match.group(1)), int(match.group(2))], raw_text=text)
        
        match = self.patterns['swap'].match(text)
        if match:
            return QuantumCommand(gate=GateType.SWAP, qubits=[int(match.group(1)), int(match.group(2))], raw_text=text)
        
        match = self.patterns['rx'].match(text)
        if match:
            angle = self._parse_angle(match.group(1))
            return QuantumCommand(gate=GateType.RX, qubits=[int(match.group(2))], params=[angle], raw_text=text)
        
        match = self.patterns['ry'].match(text)
        if match:
            angle = self._parse_angle(match.group(1))
            return QuantumCommand(gate=GateType.RY, qubits=[int(match.group(2))], params=[angle], raw_text=text)
        
        match = self.patterns['rz'].match(text)
        if match:
            angle = self._parse_angle(match.group(1))
            return QuantumCommand(gate=GateType.RZ, qubits=[int(match.group(2))], params=[angle], raw_text=text)
        
        match = self.patterns['measure'].match(text)
        if match:
            qubit = int(match.group(2))
            cbit = int(match.group(3)) if match.group(3) else None
            return QuantumCommand(gate=GateType.MEASURE, qubits=[qubit], cbits=[cbit] if cbit else None, raw_text=text)
        
        match = self.patterns['barrier'].match(text)
        if match:
            return QuantumCommand(gate=GateType.BARRIER, qubits=[], raw_text=text)
        
        match = self.patterns['bloch'].match(text)
        if match:
            return QuantumCommand(gate=GateType.BLOCH, qubits=[], raw_text=text)
        
        return None
    
    def _parse_angle(self, angle_str: str) -> float:
        """Parsea ángulo (puede ser 'pi/2', 'π', número, etc.)"""
        angle_str = angle_str.strip().replace('π', 'pi')
        
        if angle_str == 'pi':
            return 3.141592653589793
        if '/' in angle_str:
            num, den = angle_str.split('/')
            num = num.replace('pi', '3.141592653589793')
            return float(eval(num)) / float(den)
        
        try:
            return float(eval(angle_str))
        except:
            return float(angle_str)
    
    def compile(self, commands: List[str]) -> Dict:
        """Compile a list of commands for a quantum circuit"""
        parsed_commands = []
        errors = []
        
        for i, cmd in enumerate(commands):
            if not cmd.strip() or cmd.strip().startswith('#'):
                continue
            
            parsed = self.parse_command(cmd)
            if parsed:
                if parsed.gate == "CREATE" and parsed.params:
                    self.num_qubits = int(parsed.params[0])
                    self.num_cbits = self.num_qubits
                parsed_commands.append(parsed)
            else:
                errors.append(f"Línea {i+1}: Comando no reconocido '{cmd}'")
        
        self.commands = parsed_commands
        circuit = self._build_circuit()
        
        return {
            'success': len(errors) == 0,
            'circuit': circuit,
            'commands': parsed_commands,
            'errors': errors,
            'num_qubits': self.num_qubits,
            'num_cbits': self.num_cbits,
            'qasm': self.to_qasm() if circuit else None
        }
    
    def _build_circuit(self) -> Optional['QuantumCircuit']:
        """Build the Qiskit circuit from parsed commands"""
        if not HAS_QISKIT:
            raise ImportError("Qiskit is required to build circuits. Install with: pip install qiskit")
        
        if self.num_qubits == 0:
            return None
        
        qr = QuantumRegister(self.num_qubits, 'q')
        cr = ClassicalRegister(self.num_cbits, 'c')
        circuit = QuantumCircuit(qr, cr)
        
        for cmd in self.commands:
            if cmd.gate == GateType.H:
                circuit.h(cmd.qubits[0])
            elif cmd.gate == GateType.X:
                circuit.x(cmd.qubits[0])
            elif cmd.gate == GateType.Y:
                circuit.y(cmd.qubits[0])
            elif cmd.gate == GateType.Z:
                circuit.z(cmd.qubits[0])
            elif cmd.gate == GateType.S:
                circuit.s(cmd.qubits[0])
            elif cmd.gate == GateType.T:
                circuit.t(cmd.qubits[0])
            elif cmd.gate == GateType.CX:
                circuit.cx(cmd.qubits[0], cmd.qubits[1])
            elif cmd.gate == GateType.CZ:
                circuit.cz(cmd.qubits[0], cmd.qubits[1])
            elif cmd.gate == GateType.SWAP:
                circuit.swap(cmd.qubits[0], cmd.qubits[1])
            elif cmd.gate == GateType.RX:
                circuit.rx(cmd.params[0], cmd.qubits[0])
            elif cmd.gate == GateType.RY:
                circuit.ry(cmd.params[0], cmd.qubits[0])
            elif cmd.gate == GateType.RZ:
                circuit.rz(cmd.params[0], cmd.qubits[0])
            elif cmd.gate == GateType.MEASURE:
                cbit = cmd.cbits[0] if cmd.cbits else cmd.qubits[0]
                circuit.measure(cmd.qubits[0], cbit)
            elif cmd.gate == GateType.BARRIER:
                circuit.barrier()
        
        self.circuit = circuit
        return circuit
    
    def to_qasm(self) -> str:
        """Export the circuit to OpenQASM 2.0 format"""
        if not self.circuit:
            return ""
        try:
            from qiskit import qasm2
            return qasm2.dumps(self.circuit)
        except:
            return self.circuit.qasm()
    
    def simulate(self, shots: int = 1024) -> Dict:
        """Simulates the compiled circuit"""
        if not HAS_QISKIT:
            raise ImportError("Qiskit required for simulation")
        
        if not self.circuit:
            return {'error': 'No circuit compiled'}
        
        simulator = BasicSimulator()
        job = simulator.run(self.circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        return {
            'counts': counts,
            'shots': shots,
            'probabilities': {k: v/shots for k, v in counts.items()},
            'most_probable': max(counts, key=counts.get) if counts else None
        }
    
    def get_circuit_diagram(self) -> str:
        """Get the ASCII representation of the circuit"""
        if not self.circuit:
            return ""
        return str(self.circuit.draw(output='text'))

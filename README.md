```markdown
# text4q

[![PyPI version](https://badge.fury.io/py/text4q.svg)](https://badge.fury.io/py/text4q)
[![Python versions](https://img.shields.io/pypi/pyversions/text4q.svg)](https://pypi.org/project/text4q/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Write quantum circuits using plain text commands. Supports 7 human languages.**

`text4q` is a Python library that removes two barriers to quantum computing:
1. **Complex syntax** - Just write `"h 0"`, not `circuit.h(0)`
2. **Language barrier** - Use commands in English, Spanish, German, Portuguese, French, Japanese, or Chinese

Under the hood, it uses **Qiskit** for full simulation power.

---

## Installation

```bash
pip install text4q
```

Or get the latest version directly from GitHub:

```bash
pip install git+https://github.com/FerraXIDE/text4q.git
```

---

## Quick Example (Bell State)

```python
from text4q.core import Text4QCompiler

program = [
    "create 2",    # 2 qubits
    "h 0",         # Hadamard gate on qubit 0
    "cx 0 1",      # CNOT (control: 0, target: 1)
    "measure 0",   # Measure qubit 0
    "measure 1"    # Measure qubit 1
]

compiler = Text4QCompiler()
compiler.compile(program)
result = compiler.simulate(shots=1024)

print(result['counts'])
# {'00': 512, '11': 512}
```

That's it. No `QuantumCircuit(2,2)`, no `circuit.measure(0,0)`.

---

## Multi-Language Support

The same circuit works in 7 languages. Pick yours.

| Language | "create" | "barrier" | "measure" |
|----------|----------|-----------|-----------|
| English | `create` | `barrier` | `measure` |
| Spanish | `crear` | `barrera` | `medir` |
| German | `erstelle` | `barriere` | `messen` |
| Portuguese | `criar` | `barreira` | `medir` |
| French | `créer` | `barrière` | `mesurer` |
| Japanese | `作成` | `バリア` | `測定` |
| Chinese | `创建` | `屏障` | `测量` |

---

## Supported Gates

| Command | Description |
|---------|-------------|
| `h 0` | Hadamard (superposition) |
| `x 0` | NOT gate (flip) |
| `y 0` | Y gate (bit + phase flip) |
| `z 0` | Z gate (phase flip) |
| `cx 0 1` | CNOT (control: 0, target: 1) |
| `cz 0 1` | Controlled-Z |
| `swap 0 1` | Swaps two qubits |
| `rx(pi/2) 0` | Rotation around X axis |
| `ry(pi/4) 0` | Rotation around Y axis |
| `rz(pi) 0` | Rotation around Z axis |
| `measure 0` | Measures qubit 0 |
| `barrier` | Visual separator for diagrams |

**Angle shortcuts:** Use `pi`, `pi/2`, `pi/4`, or any number.

---

## Full Example: Rotation Gates

```python
from text4q.core import Text4QCompiler

program = [
    "create 1",
    "rx(pi/2) 0",    # 90-degree rotation around X
    "ry(pi/4) 0",    # 45-degree rotation around Y
    "measure 0"
]

compiler = Text4QCompiler()
compiler.compile(program)
print(compiler.simulate(shots=1000)['counts'])
```

---

## See the Circuit Diagram

```python
from text4q.core import Text4QCompiler

program = ["create 2", "h 0", "cx 0 1", "measure 0", "measure 1"]
compiler = Text4QCompiler()
compiler.compile(program)

print(compiler.circuit.draw(output='text'))
```

Output:

```
     ┌───┐     ┌─┐   
q_0: ┤ H ├──■──┤M├───
     └───┘┌─┴─┐└╥┘┌─┐
q_1: ─────┤ X ├─╫─┤M├
          └───┘ ║ └╥┘
c: 2/═══════════╩══╩═
                0  1 
```

---

## Why text4q?

**Zero learning curve** – If you know the gates, you know text4q  
**Multi-language** – 7 human languages supported  
**Great for teaching** – Students focus on concepts, not syntax  
**Quick prototyping** – Write quantum algorithms in seconds  
**Same power as Qiskit** – Compiles to Qiskit under the hood  

**Not a replacement for Qiskit** – For very complex or dynamic circuits, use Qiskit directly.

---

## Roadmap

- [ ] More languages (Italian, Korean, Hindi, Arabic)
- [ ] Even simpler syntax for common algorithms (Grover, Shor)
- [ ] Better error messages in your native language

---

## Contributing

Contributions are welcome! Open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

---

## Links

- [GitHub Repository](https://github.com/FerraXIDE/text4q)
- [PyPI Page](https://pypi.org/project/text4q/)
- [Report an Issue](https://github.com/FerraXIDE/text4q/issues)

---

*Made with ❤️ and qubits*

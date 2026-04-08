# text4q/__init__.py
"""
text4q - Natural command language for quantum computing
"""

from .core import Text4QCompiler
from .core import HAS_QISKIT

__all__ = ['Text4QCompiler', 'HAS_QISKIT']

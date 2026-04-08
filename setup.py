from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text4q",
    version="1.0.3",
    author="Gabriel De Jesús Sánchez Ferra",
    author_email="gabrielsanchezferra@gmail.com",
    description="Natural command language for quantum computing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FerraXIDE/text4q",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "qiskit>=0.45.0",
        "numpy>=1.24.0",
    ],
)

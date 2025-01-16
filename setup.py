from setuptools import find_packages, setup

setup(
    name="dataviewer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pytest>=7.0.0",],
    python_requires=">=3.7",
    author="suizongbuhenatie",
    description="A Python library for creating nested visualizations",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

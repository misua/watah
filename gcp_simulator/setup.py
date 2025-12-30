from setuptools import setup, find_packages

setup(
    name="activity-simulator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pywin32>=306",
        "pynput>=1.7.6",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "PyYAML>=6.0",
        "click>=8.1.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "activity-sim=activity_simulator.cli:main",
        ],
    },
    python_requires=">=3.8",
)

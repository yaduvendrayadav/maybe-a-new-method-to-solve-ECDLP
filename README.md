# Discrete Logarithm Problem Solver

This repository contains a Python script that solves the discrete logarithm problem using the Chinese remainder theorem and SageMath. The discrete logarithm problem is a fundamental problem in cryptography and number theory.

## Motive

The motive of this project is to provide a simple implementation of a discrete logarithm problem solver. The code uses efficient algorithms to find congruences and solve linear systems of equations, allowing for the efficient solution of the discrete logarithm problem in certain cases.

## Features

- Generates and solves congruences in accordance with Hoffstein, Pipher, Silverman's method.
- Converts the linear system to dense matrices for solving using SageMath.
- Checks congruences and verifies the solutions.
- Searches for an additional parameter that satisfies a B-smooth condition.
- Solves the main discrete logarithm problem.

## Requirements

- Python 3.x
- SageMath (https://www.sagemath.org/)
- primefac library (https://pypi.org/project/primefac/)

## Usage

1. Install Python 3.x and SageMath on your system.
2. Install the primefac library by running `pip install primefac`.
3. Clone this repository or download the `discrete_logarithm_solver.py` file.
4. Open a terminal or command prompt and navigate to the directory where the file is located.
5. Run the script using the command `python discrete_logarithm_solver.py`.

Note: The script requires SageMath to solve the linear system of equations. Make sure the `sage` command is available in your system's PATH.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

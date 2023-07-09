import math
import random
import multiprocessing
import numpy as np

# Constants for SECP256K1 curve
curve_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
base_point = (str(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798),
              str(0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8))


def quadratic_sieve(n):
    # Quadratic Sieve algorithm implementation
    # Factorize the number 'n' into small factors
    # Returns a list of small factors of 'n'
    # (Simplified implementation)

    factors = []

    # Perform factorization
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i

    # Check if any remaining factor exists
    if n > 1:
        factors.append(n)

    return factors


def pollards_kangaroo(params):
    # Pollard's Kangaroo algorithm implementation for a single factor
    # Compute the discrete logarithm of 'target_point' with respect to 'base_point'
    # Returns the factor and the discrete logarithm

    factor, target_point = params

    # Set the maximum number of jumps and the step size
    max_jumps = 100000
    step_size = 20

    # Initialize the kangaroo's positions
    kangaroo_a = random.randint(1, curve_order - 1)
    kangaroo_b = kangaroo_a

    # Perform the random walks
    for i in range(max_jumps):
        for _ in range(step_size):
            kangaroo_a = (kangaroo_a + int(base_point[0])) % curve_order
            kangaroo_b = (kangaroo_b + int(target_point[0])) % curve_order

            if kangaroo_a == kangaroo_b:
                break

        if kangaroo_a == kangaroo_b:
            break

    # Compute the discrete logarithm
    discrete_log = (kangaroo_a - kangaroo_b) % curve_order

    return factor, discrete_log


def combine_results(results, small_factors, curve_order):
    # Combine the results obtained modulo small factors
    # Using Chinese Remainder Theorem (CRT)
    # Returns the final discrete logarithm

    # Compute the product of all small factors
    product = 1
    for factor in small_factors:
        product *= factor

    # Compute the inverse of each factor modulo the curve order
    inverses = []
    for factor in small_factors:
        inverse = pow(product // factor, -1, factor)
        inverses.append(inverse)

    # Apply the CRT to combine the results
    combined_result = 0
    for i in range(len(results)):
        combined_result += results[i][1] * (product // small_factors[i]) * inverses[i]

    return combined_result % curve_order


# Example usage
public_key = input("Enter the public key in hexadecimal format: ")
public_key = (str(int(public_key[:64], 16)), str(int(public_key[64:], 16)))

print("Finding small factors using Quadratic Sieve...")
# Step 1: Use the Quadratic Sieve algorithm to find small factors
small_factors = quadratic_sieve(curve_order)
print("Small factors:", small_factors)

print("Computing discrete logarithm modulo each small factor using Pollard's Kangaroo...")
# Step 2: Compute the discrete logarithm modulo each small factor using Pollard's Kangaroo algorithm
pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
results = pool.map(pollards_kangaroo, [(factor, public_key) for factor in small_factors])

print("Results modulo small factors:", results)

print("Combining the results using Chinese Remainder Theorem (CRT)...")
# Step 3: Combine the results using the Chinese Remainder Theorem (CRT)
final_discrete_log = combine_results(results, small_factors, curve_order)

print("Discrete logarithm:", final_discrete_log)

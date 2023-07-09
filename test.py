import math
import random

# Constants for SECP256K1 curve
curve_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
base_point = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
              0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


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


def pollards_kangaroo(curve_order, base_point, target_point):
    # Pollard's Kangaroo algorithm implementation
    # Compute the discrete logarithm of 'target_point' with respect to 'base_point'
    # Returns the discrete logarithm

    # Set the maximum number of jumps and the step size
    max_jumps = 100000
    step_size = 20

    # Initialize the kangaroo's positions
    kangaroo_a = random.randint(1, curve_order - 1)
    kangaroo_b = kangaroo_a

    # Perform the random walks
    for i in range(max_jumps):
        for _ in range(step_size):
            kangaroo_a = (kangaroo_a + base_point[0]) % curve_order
            kangaroo_b = (kangaroo_b + target_point[0]) % curve_order

            if kangaroo_a == kangaroo_b:
                break

        if kangaroo_a == kangaroo_b:
            break

    # Compute the discrete logarithm
    discrete_log = (kangaroo_a - kangaroo_b) % curve_order

    return discrete_log


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
        combined_result += results[i] * (product // small_factors[i]) * inverses[i]

    return combined_result % curve_order


# Example usage
target_point = (0x6CBB85C4C8F8B7FC09F647C9CD9A2A760B5D6A8E179859F572C9E11C72339F6A,
                0x8D85060C3E67516B566F3A5C6EF4F38F6B04F4E08C3D05F2A1C3F58C84E86663)

# Step 1: Use the Quadratic Sieve algorithm to find small factors
small_factors = quadratic_sieve(curve_order)

# Step 2: Compute the discrete logarithm modulo each small factor using Pollard's Kangaroo algorithm
results = []
for factor in small_factors:
    discrete_log = pollards_kangaroo(factor, base_point, target_point)
    results.append(discrete_log)

# Step 3: Combine the results using the Chinese Remainder Theorem (CRT)
final_discrete_log = combine_results(results, small_factors, curve_order)

print("Discrete logarithm:", final_discrete_log)

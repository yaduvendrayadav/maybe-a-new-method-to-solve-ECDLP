import math
import random


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
            kangaroo_a = (kangaroo_a + base_point) % curve_order
            kangaroo_b = (kangaroo_b + target_point) % curve_order

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
curve_order = 383  # Example curve order
base_point = 5  # Example base point
target_point = 281  # Example target point

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

import subprocess
from random import randint
from ast import literal_eval
from primefac import primefac
from math import exp, sqrt, log

# Define the parameters
g = 37
h = 211
p = 18443
B = 5
max_equations = 6

# L complexity notation
def L(x): return exp(log(x)*sqrt(log(log(x))))

# Determine if n is B-smooth (uses fast factoring)
def is_Bsmooth(b, n):
    P = list(primefac(n))
    if len(P) != 0 and P[-1] <= b: 
        return True, P
    else: return False, P

# Euclidean modular inverse
def euclid_modinv(b, n):
    x0, x1 = 1, 0
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
    return x0

# Convert a list of prime factors (with repetition) to 
# a dictionary of prime factors and their exponents.
def factorlist_to_explist(L):
    D = {}
    for n in L:
        try: D[int(n)] += 1
        except: D[int(n)] = 1
    return {base : D[base] for base in D.keys()}

# Chinese remainder theorem
def chinese_remainder(n, a):
    prod = reduce(lambda a, b: a*b, n)
    f = lambda a_i, n_i: a_i * euclid_modinv(prod // n_i, n_i) * (prod // n_i) 
    return sum([f(a_i, n_i) for n_i, a_i in zip(n, a)]) % prod

# Find congruences in accordance with Hoffstein, Phipher, Silverman (3.32)
def find_congruences(congruences=[], bases=[]):
    unique = lambda l: list(set(l))
    while True:                                                    
        k = randint(2, p)                                                          
        _ = is_Bsmooth(B, pow(g,k,p))                                             
        if _[0]:                                                                   
            congruences.append((factorlist_to_explist(_[1]),k))                    
            bases = unique([base for c in [c[0].keys() for c in congruences] for base in c])
            if len(congruences) >= max_equations: break
    print('congruences: {}\nbases: {}'.format(len(congruences), len(bases)))
    return bases, congruences

# Convert the linear system to dense matrices 
def to_matrices(bases, congruences):
    M = [[c[0][base] if base in c[0] else 0 for base in bases] for c in congruences]
    b = [c[1] for c in congruences]
    return M, b

# Use SageMath to solve (potentially) big systems of equations
def msolve(M, b):
    sage_cmd = '''L1 = {};
L2 = {};
R = IntegerModRing({});
M = Matrix(R, L1);
b = vector(R, L2);
print(M.solve_right(b))'''.format(M, b, p-1)
    with open('run.sage', 'w') as output_file:
        output_file.write(sage_cmd)
    cmd_result = subprocess.getstatusoutput('sage ./run.sage')
    if cmd_result[0] != 0:
        print('Sage failed with error {}'.format(cmd_result[0]))
        exit()
    return literal_eval(cmd_result[1])

# Solve a linear equation 
def evaluate(eq, dlogs):
    return sum([dlogs[term] * exp for term, exp in eq.items()]) % (p-1)

# Check congruences
def check_congruences(congruences, dlogs):
    print('Checking congruences:', end=" ")
    passed = True
    for c in congruences:
        if evaluate(c[0], dlogs) != c[1]:
            passed = False
    if passed:
        print('Passed!\n')
    else:
        print('Failed, try running again?')
        exit()
    return passed

# Check dlog exponents
def check_dlogs(exponents, bases):
    print('Checking dlog exponents:')
    passed = True 
    for exponent, base in zip(exponents, bases):
        if pow(g, exponent, p) != base:
            passed = False
        else:
            print('{}^{} = {} (mod {})'.format(g, exponent, base, p))
    if passed:
        print('Passed!\n')
    else:
        print('Failed, try running again.')
        exit()
    return passed

def main():
    # Generate and solve congruences
    print('p: {}, g: {}, h: {}, B: {}'.format(p, g, h, B))
    print('Searching for congruences.')
    bases, congruences = find_congruences()
    print('Converting to matrix format.')
    M, b = to_matrices(bases, congruences)
    print('Solving linear system with Sage:')
    exponents = msolve(M, b)
    print('Sage done.')

    # Dictionary of bases and exponents
    dlogs = {b: exp for (b, exp) in zip(bases, exponents)}

    # Verify the results
    check_congruences(congruences, dlogs)
    check_dlogs(exponents, bases)

    print('Searching for k such that h * g^-k is B-smooth.')
    for i in range(10**9):
        k = randint(2, p)
        c = is_Bsmooth(B, (h * pow(euclid_modinv(g, p), k)) % p)
        if c[0]:
            print('Found k = {}'.format(k))
            break

    print('Solving the main dlog problem:\n')
    soln = (evaluate(factorlist_to_explist(c[1]), dlogs) + k) % (p-1)
    if pow(g, soln, p) == h:
        print('{}^{} = {} (mod {}) holds!'.format(g, soln, h, p))
        print('DLP solution: {}'.format(soln))
    else:
        print('Failed.')

if __name__ == '__main__':
    main()

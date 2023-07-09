# maybe-a-new-method-to-solve-ECDLP

the code is imperfect but the motive of the code is

 Step 1: Use the Quadratic Sieve algorithm to find small factors
 Step 2: Compute the discrete logarithm modulo each small factor using Pollard's Kangaroo algorithm
 Step 3: Combine the results using the Chinese Remainder Theorem (CRT)

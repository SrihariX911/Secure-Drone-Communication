# Polynomial Module
from operator import add, neg, mod
from fractions import Fraction as frac
from numpy.polynomial import polynomial as P

# Resize function adds leading zeros to polynomial vectors
def resize(c1, c2):
    """
    Resize two polynomial lists to have the same length by appending zeros to the shorter one.
    
    Parameters:
        c1 (list): First polynomial.
        c2 (list): Second polynomial.

    Returns:
        list: List containing the resized polynomials.
    """
    if len(c1) > len(c2):
        c2 = c2 + [0] * (len(c1) - len(c2))
    if len(c1) < len(c2):
        c1 = c1 + [0] * (len(c2) - len(c1))
    return [c1, c2]

# Removes leading zeros from the polynomial
def trim(seq):
    """
    Removes leading zeros from the polynomial.
    
    Parameters:
        seq (list): The polynomial list to trim.
        
    Returns:
        list: Trimmed polynomial.
    """
    if len(seq) == 0:
        return seq
    else:
        for i in range(len(seq) - 1, -1, -1):
            if seq[i] != 0:
                break
        return seq[:i + 1]

# Subtracts two polynomials
def subPoly(c1, c2):
    """
    Subtracts two polynomials.

    Parameters:
        c1 (list): First polynomial.
        c2 (list): Second polynomial.

    Returns:
        list: Resultant polynomial after subtraction.
    """
    c1, c2 = resize(c1, c2)
    c2 = list(map(neg, c2))
    out = list(map(add, c1, c2))
    return trim(out)

# Adds two polynomials
def addPoly(c1, c2):
    """
    Adds two polynomials.
    
    Parameters:
        c1 (list): First polynomial.
        c2 (list): Second polynomial.

    Returns:
        list: Resultant polynomial after addition.
    """
    c1, c2 = resize(c1, c2)
    out = list(map(add, c1, c2))
    return trim(out)

# Multiplies two polynomials
def multPoly(c1, c2):
    """
    Multiplies two polynomials.
    
    Parameters:
        c1 (list): First polynomial.
        c2 (list): Second polynomial.

    Returns:
        list: Resultant polynomial after multiplication.
    """
    order = (len(c1) - 1 + len(c2) - 1)
    out = [0] * (order + 1)
    for i in range(len(c1)):
        for j in range(len(c2)):
            out[j + i] += c1[i] * c2[j]
    return trim(out)

# Divides two polynomials
def divPoly(N, D):
    """
    Divides two polynomials using polynomial long division.
    
    Parameters:
        N (list): Numerator polynomial.
        D (list): Denominator polynomial.

    Returns:
        list: Quotient and remainder polynomials.
    """
    N, D = list(map(frac, trim(N))), list(map(frac, trim(D)))
    degN, degD = len(N) - 1, len(D) - 1
    if degN >= degD:
        q = [0] * (degN - degD + 1)
        while degN >= degD and N != [0]:
            d = list(D)
            [d.insert(0, frac(0, 1)) for _ in range(degN - degD)]
            q[degN - degD] = N[degN] / d[-1]
            d = [x * q[degN - degD] for x in d]
            N = subPoly(N, d)
            degN = len(N) - 1
        r = N
    else:
        q = [0]
        r = N
    return [trim(q), trim(r)]

# Polynomial coefficients modulo k
def modPoly(c, k):
    """
    Computes the polynomial coefficients modulo k.
    
    Parameters:
        c (list): Polynomial coefficients.
        k (int): Modulus.
    
    Returns:
        list: Polynomial coefficients modulo k.
    """
    if k == 0:
        raise ValueError("Error: Modulus k must be non-zero.")
    else:
        return [fracMod(x, k) for x in c]

# Centerlift of Polynomial with respect to q
def cenPoly(c, q):
    """
    Computes the center-lift of a polynomial with respect to q.
    
    Parameters:
        c (list): Polynomial coefficients.
        q (int): The value to center the polynomial around.
    
    Returns:
        list: Center-lifted polynomial.
    """
    u = float(q) / 2
    l = -u
    c = modPoly(c, q)
    c = [mod(x, -q) if x > u else x for x in c]
    c = [mod(x, q) if x <= l else x for x in c]
    return c

# Extended Euclidean Algorithm for Polynomials
def extEuclidPoly(a, b):
    """
    Extended Euclidean algorithm for polynomials. It computes the GCD of two polynomials
    and the coefficients s and t such that a*s + b*t = GCD(a, b).
    
    Parameters:
        a (list): First polynomial.
        b (list): Second polynomial.
    
    Returns:
        list: GCD of a and b, coefficients s and t.
    """
    switch = False
    a = trim(a)
    b = trim(b)
    if len(a) >= len(b):
        a1, b1 = a, b
    else:
        a1, b1 = b, a
        switch = True

    Q, R = [], []
    while b1 != [0]:
        q, r = divPoly(a1, b1)
        Q.append(q)
        R.append(r)
        a1 = b1
        b1 = r

    S = [0] * (len(Q) + 2)
    T = [0] * (len(Q) + 2)

    S[0], S[1], T[0], T[1] = [1], [0], [0], [1]

    for x in range(2, len(S)):
        S[x] = subPoly(S[x - 2], multPoly(Q[x - 2], S[x - 1]))
        T[x] = subPoly(T[x - 2], multPoly(Q[x - 2], T[x - 1]))

    gcd_val = R[-2]
    s_out = S[-2]
    t_out = T[-2]
    
    # Scaling GCD such that the leading term has coefficient 1
    scale_factor = gcd_val[-1]
    gcd_val = [x / scale_factor for x in gcd_val]
    s_out = [x / scale_factor for x in s_out]
    t_out = [x / scale_factor for x in t_out]
    
    if switch:
        return [gcd_val, t_out, s_out]
    else:
        return [gcd_val, s_out, t_out]

# Check if a polynomial is ternary
def isTernary(f, alpha, beta):
    """
    Checks if a polynomial is ternary based on its coefficients.
    
    Parameters:
        f (list): Polynomial coefficients.
        alpha (int): Number of +1 coefficients.
        beta (int): Number of -1 coefficients.
    
    Returns:
        bool: True if the polynomial is ternary, False otherwise.
    """
    ones = f.count(1)
    negones = f.count(-1)
    if (negones + ones) <= len(f) and alpha == ones and beta == negones:
        return True
    else:
        return False

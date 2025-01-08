# Polynomial Module
from operator import add, neg, mod
from fractions import Fraction as frac

# Resize function adds leading zeros to polynomial vectors
def resize(c1, c2):
    """
    Resizes two polynomial lists to have the same length by appending zeros to the shorter one.
    
    Parameters:
        c1 (list): Coefficients of the first polynomial.
        c2 (list): Coefficients of the second polynomial.

    Returns:
        list: Resized polynomial lists.
    """
    if len(c1) > len(c2):
        c2 += [0] * (len(c1) - len(c2))
    elif len(c1) < len(c2):
        c1 += [0] * (len(c2) - len(c1))
    return [c1, c2]

# Removes leading zeros from a polynomial
def trim(seq):
    """
    Removes leading zeros from a polynomial coefficient list.
    
    Parameters:
        seq (list): Polynomial coefficients.

    Returns:
        list: Trimmed polynomial coefficients.
    """
    return seq[:next((i + 1 for i in reversed(range(len(seq))) if seq[i] != 0), 0)]

# Subtracts two polynomials
def subPoly(c1, c2):
    """
    Subtracts the coefficients of two polynomials.
    
    Parameters:
        c1 (list): Coefficients of the first polynomial.
        c2 (list): Coefficients of the second polynomial.

    Returns:
        list: Resultant polynomial after subtraction.
    """
    c1, c2 = resize(c1, c2)
    c2 = list(map(neg, c2))
    return trim(list(map(add, c1, c2)))

# Adds two polynomials
def addPoly(c1, c2):
    """
    Adds the coefficients of two polynomials.
    
    Parameters:
        c1 (list): Coefficients of the first polynomial.
        c2 (list): Coefficients of the second polynomial.

    Returns:
        list: Resultant polynomial after addition.
    """
    c1, c2 = resize(c1, c2)
    return trim(list(map(add, c1, c2)))

# Multiplies two polynomials
def multPoly(c1, c2):
    """
    Multiplies two polynomials and returns their product.
    
    Parameters:
        c1 (list): Coefficients of the first polynomial.
        c2 (list): Coefficients of the second polynomial.

    Returns:
        list: Resultant polynomial after multiplication.
    """
    order = len(c1) + len(c2) - 2
    out = [0] * (order + 1)
    for i, coeff1 in enumerate(c1):
        for j, coeff2 in enumerate(c2):
            out[i + j] += coeff1 * coeff2
    return trim(out)

# Divides two polynomials using long division
def divPoly(N, D):
    """
    Divides two polynomials using polynomial long division.

    Parameters:
        N (list): Coefficients of the numerator polynomial.
        D (list): Coefficients of the denominator polynomial.

    Returns:
        list: Quotient and remainder polynomials.
    """
    N, D = list(map(frac, trim(N))), list(map(frac, trim(D)))
    q = [0] * (len(N) - len(D) + 1) if len(N) >= len(D) else [0]
    while len(N) >= len(D) and N != [0]:
        factor = N[-1] / D[-1]
        q[len(N) - len(D)] = factor
        N = subPoly(N, [0] * (len(N) - len(D) - 1) + [factor * coeff for coeff in D])
    return [trim(q), trim(N)]

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
        raise ValueError("Modulus k must be non-zero.")
    return [fracMod(x, k) for x in c]

# Centerlift of a polynomial with respect to q
def cenPoly(c, q):
    """
    Computes the center-lift of a polynomial with respect to q.
    
    Parameters:
        c (list): Polynomial coefficients.
        q (int): Modulus.

    Returns:
        list: Center-lifted polynomial coefficients.
    """
    mid = q / 2
    c = modPoly(c, q)
    return [mod(x, q) if x > mid else mod(x, -q) for x in c]

# Extended Euclidean Algorithm for Polynomials
def extEuclidPoly(a, b):
    """
    Computes the GCD of two polynomials and their coefficients such that:
        a*s + b*t = GCD(a, b)
    
    Parameters:
        a (list): Coefficients of the first polynomial.
        b (list): Coefficients of the second polynomial.

    Returns:
        list: GCD of a and b, coefficients s and t.
    """
    a, b = trim(a), trim(b)
    if len(a) < len(b):
        a, b = b, a
        switched = True
    else:
        switched = False

    Q, R = [], []
    while b:
        q, r = divPoly(a, b)
        Q.append(q)
        R.append(r)
        a, b = b, r

    S, T = [[1], [0]], [[0], [1]]
    for q in Q:
        S.append(subPoly(S[-2], multPoly(q, S[-1])))
        T.append(subPoly(T[-2], multPoly(q, T[-1])))

    gcd_val = R[-2]
    scale = gcd_val[-1]
    gcd_val, s_out, t_out = [
        [coeff / scale for coeff in poly] for poly in (gcd_val, S[-2], T[-2])
    ]

    return [gcd_val, t_out, s_out] if switched else [gcd_val, s_out, t_out]

# Checks if a polynomial is ternary
def isTernary(f, alpha, beta):
    """
    Checks if a polynomial is ternary (contains exactly `alpha` +1 and `beta` -1).

    Parameters:
        f (list): Polynomial coefficients.
        alpha (int): Expected number of +1 coefficients.
        beta (int): Expected number of -1 coefficients.

    Returns:
        bool: True if ternary, False otherwise.
    """
    ones, neg_ones = f.count(1), f.count(-1)
    return ones == alpha and neg_ones == beta and ones + neg_ones <= len(f)

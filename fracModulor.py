# Helper Functions
# Extended Euclidean Algorithm for Integers
from fractions import Fraction as frac

def egcd(a, b):
    """
    Extended Euclidean Algorithm to find the GCD of two integers
    and coefficients (x, y) such that ax + by = gcd(a, b).

    Parameters:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        tuple: (gcd, x, y) where gcd is the greatest common divisor of a and b,
               and x, y are the coefficients.
    """
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd_val = b
    return gcd_val, x, y

# Modular Inverse Function
# An application of the extended GCD algorithm to find modular inverses
def modinv(a, m):
    """
    Finds the modular inverse of 'a' under modulo 'm'.

    Parameters:
        a (int): The number to find the modular inverse of.
        m (int): The modulus.

    Returns:
        int or None: Modular inverse of 'a' under 'm' if it exists, otherwise None.
    """
    gcd_val, x, _ = egcd(a, m)
    if gcd_val != 1:
        return None  # Modular inverse does not exist
    return x % m

# Modulus Function to Handle Fractions
def frac_mod(f, m):
    """
    Computes the modulus of a fraction under a given modulus 'm'.
    Handles cases where the denominator and modulus are coprime.

    Parameters:
        f (Fraction): The fraction to compute the modulus for.
        m (int): The modulus.

    Returns:
        int: Result of (numerator * modular_inverse(denominator)) % m.

    Raises:
        ValueError: If the denominator and modulus are not coprime.
    """
    gcd_val, _, _ = egcd(f.denominator, m)
    if gcd_val != 1:
        raise ValueError("ERROR: GCD of the denominator and modulus is not 1.")
    else:
        return modinv(f.denominator, m) * f.numerator % m

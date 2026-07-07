import math

def is_prime(n):
    """Checks if a number is a prime number."""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def extended_gcd(a, b):
    """
    The Extended Euclidean Algorithm.
    This does the heavy lifting to find the secret Private Key (the modular inverse).
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1  
    """WE want ans as gcd=1 let a=2, b=3, x1=1 , y1=0
    b//a =1
    (b // a) * x1=1
    y1 - (b // a) * x1 = 0-1=-1
    
    but if we do y1%x1 0%1 =0 so not correct so we need to return y1 - (b // a) * x1 as x and x1 as y

    """
    y = x1
    return gcd, x, y

def get_modular_inverse(e, phi):
    """Calculates 'd' so that (e * d) % phi == 1"""
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        # We use modulo phi to ensure the result is positive
        return x % phi

def generate_rsa_keys(p, q):
    """Generates both Public and Private keys given two prime numbers."""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both inputs must be prime numbers.")
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # We pick 3 as a standard starting public exponent
    e = 3 
    while math.gcd(e, phi) != 1:
        e += 2
        
    # Calculate the private decryption key
    d = get_modular_inverse(e, phi)
    
    # Return everything neatly packaged for our Django views
    return {
        'public_e': e,
        'public_n': n,
        'private_d': d
    }
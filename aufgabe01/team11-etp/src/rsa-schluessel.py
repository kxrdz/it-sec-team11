from sympy import isprime, randprime
from math import gcd

# Schritt 1: Primzahlen wählen
p = randprime(2**255, 2**256)
q = randprime(2**255, 2**256)

# Schritt 2: N berechnen
N = p * q

# Schritt 3: Phi berechnen
phi = (p - 1) * (q - 1)

# Schritt 4: e wählen
e = 65537
assert gcd(e, phi) == 1

# Schritt 5: d berechnen
d = pow(e, -1, phi)

anzahl_bits = N.bit_length()

print(f'N ist {anzahl_bits} bits')
with open("pubkey", "w") as file:
    file.write(f"e:{e}\nN: {N}")

with open("privkey", "w") as file:
    file.write(f"d:{d}\nN:{N}")

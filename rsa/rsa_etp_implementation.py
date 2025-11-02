
# ============================================================
# PYTHON IMPLEMENTATION CODE EXAMPLES
# ============================================================

# -------------------- 1. CRYPTO UTILITIES --------------------

def gcd(a, b):
    '''
    Berechnet den größten gemeinsamen Teiler (ggT) von a und b
    '''
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    '''
    Erweiterter Euklidischer Algorithmus
    Findet x und y sodass: a*x + b*y = gcd(a,b)

    Rückgabe: (gcd, x, y)
    '''
    if b == 0:
        return (a, 1, 0)
    else:
        gcd_val, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (gcd_val, x, y)


def mod_inverse(e, phi):
    '''
    Berechnet das modulare multiplikative Inverse von e modulo phi
    Nutzt den erweiterten Euklidischen Algorithmus

    Gibt d zurück sodass: (e * d) mod phi = 1
    '''
    gcd_val, x, y = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Modulares Inverses existiert nicht")
    return x % phi


def modpow(base, exponent, modulus):
    '''
    Modulare Exponentiation: (base^exponent) mod modulus
    Nutzt Binary Exponentiation für Effizienz

    Wichtig: Eigene Implementierung für den Bonuspunkt!
    '''
    result = 1
    base = base % modulus

    while exponent > 0:
        # Wenn Exponent ungerade, multipliziere mit base
        if exponent % 2 == 1:
            result = (result * base) % modulus

        # Halbiere den Exponenten (Integer Division)
        exponent = exponent >> 1  # oder: exponent // 2

        # Quadriere die Basis
        base = (base * base) % modulus

    return result


# -------------------- 2. PRIME GENERATION --------------------

import random

def is_prime_miller_rabin(n, k=40):
    '''
    Miller-Rabin Primzahltest
    n: zu testende Zahl
    k: Anzahl der Testrunden (höher = genauer)

    Rückgabe: True wenn wahrscheinlich prim, False wenn sicher nicht prim
    '''
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Schreibe n-1 als 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Führe k Testrunden durch
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # Hier darf pow() genutzt werden (nur für Primtest)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_prime(bits):
    '''
    Generiert eine zufällige Primzahl mit der angegebenen Bitlänge
    '''
    while True:
        # Generiere zufällige ungerade Zahl
        num = random.getrandbits(bits)
        # Setze höchstes Bit (für richtige Länge)
        num |= (1 << (bits - 1))
        # Setze niedrigstes Bit (macht Zahl ungerade)
        num |= 1

        if is_prime_miller_rabin(num):
            return num


# -------------------- 3. RSA KEY GENERATION --------------------

def generate_rsa_keypair(bits=512):
    '''
    Generiert ein RSA Schlüsselpaar

    Parameter:
        bits: Bitlänge des Modulus n (512 für diese Aufgabe)

    Rückgabe:
        ((e, n), (d, n)) - (public_key, private_key)
    '''
    # Generiere zwei Primzahlen p und q (je bits/2 Bits)
    print("Generiere Primzahl p...")
    p = generate_prime(bits // 2)

    print("Generiere Primzahl q...")
    q = generate_prime(bits // 2)

    # Stelle sicher dass p != q
    while p == q:
        q = generate_prime(bits // 2)

    # Berechne n = p * q
    n = p * q

    # Berechne Eulers Totient φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Wähle öffentlichen Exponenten e
    # Standard: 65537 (0x10001) - sicher und effizient
    e = 65537

    # Prüfe ob gcd(e, phi) = 1
    if gcd(e, phi) != 1:
        # Falls nicht, wähle andere Primzahlen
        return generate_rsa_keypair(bits)

    # Berechne privaten Exponenten d
    # d ist das modulare Inverse von e modulo phi
    print("Berechne privaten Schlüssel...")
    d = mod_inverse(e, phi)

    # Verifiziere: (e * d) mod phi = 1
    assert (e * d) % phi == 1, "Schlüsselgenerierung fehlgeschlagen!"

    print(f"Schlüsselpaar generiert!")
    print(f"p: {bits//2} bits")
    print(f"q: {bits//2} bits")
    print(f"n: {n.bit_length()} bits")

    return ((e, n), (d, n))


# -------------------- 4. ENCRYPTION/DECRYPTION --------------------

def rsa_encrypt(message_int, public_key):
    '''
    RSA Verschlüsselung

    Parameter:
        message_int: Nachricht als Integer
        public_key: (e, n)

    Rückgabe:
        ciphertext als Integer
    '''
    e, n = public_key
    return modpow(message_int, e, n)


def rsa_decrypt(ciphertext_int, private_key):
    '''
    RSA Entschlüsselung

    Parameter:
        ciphertext_int: Ciphertext als Integer
        private_key: (d, n)

    Rückgabe:
        plaintext als Integer
    '''
    d, n = private_key
    return modpow(ciphertext_int, d, n)


def bytes_to_int(data):
    '''Konvertiert Bytes zu Integer (Big-Endian)'''
    return int.from_bytes(data, byteorder='big')


def int_to_bytes(num, length):
    '''Konvertiert Integer zu Bytes (Big-Endian)'''
    return num.to_bytes(length, byteorder='big')


# -------------------- 5. ETP SERVER --------------------

import socket

def announce_server(port):
    '''
    Schritt 1: Kündige Server bei 10.42.1.23:3033 an
    '''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('10.42.1.23', 3033))

        # Sende Portnummer als ASCII
        message = str(port).encode('ascii')
        sock.sendall(message)

        # Warte auf "Ok" Antwort
        response = sock.recv(1024).decode('ascii')
        sock.close()

        if response.strip() == "Ok":
            print(f"Server erfolgreich angekündigt auf Port {port}")
            return True
        else:
            print(f"Unerwartete Antwort: {response}")
            return False
    except Exception as e:
        print(f"Fehler bei Serverankündigung: {e}")
        return False


def run_etp_server(port, public_key, private_key):
    '''
    Hauptfunktion für ETP Server

    Parameter:
        port: Port auf dem Server lauscht
        public_key: (e, n)
        private_key: (d, n)
    '''
    e, n = public_key
    d, _ = private_key

    # Erstelle Server Socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', port))
    server_sock.listen(1)

    print(f"ETP Server läuft auf Port {port}")
    print("Warte auf Verbindung...")

    try:
        while True:
            # Akzeptiere Client Verbindung
            client_sock, client_addr = server_sock.accept()
            print(f"Verbindung von {client_addr}")

            try:
                # Empfange Kommando
                data = client_sock.recv(1024).decode('ascii').strip()
                print(f"Empfangen: {data}")

                # Prüfe Kommando
                if data == "GET pubkey ETP/2025":
                    # Sende Public Key
                    response = f"pub: {e:x}\\nN: {n:x}\\n"
                    client_sock.sendall(response.encode('ascii'))
                    print("Public Key gesendet")

                    # Empfange verschlüsselte Nachricht
                    ciphertext_hex = client_sock.recv(4096).decode('ascii').strip()
                    print(f"Ciphertext empfangen: {len(ciphertext_hex)} Zeichen")

                    # Konvertiere von Hex zu Integer
                    ciphertext = int(ciphertext_hex, 16)

                    # Entschlüssele
                    plaintext_int = rsa_decrypt(ciphertext, private_key)

                    # Konvertiere zu Bytes
                    plaintext_bytes = int_to_bytes(plaintext_int, 64)  # 512 bits = 64 bytes

                    # Entferne Null-Padding und dekodiere UTF-8
                    plaintext = plaintext_bytes.rstrip(b'\\x00').decode('utf-8')

                    # Ausgabe auf stdout
                    print(f"Entschlüsselte Nachricht: {plaintext}")

                elif data.startswith("GET"):
                    # Ungültige Ressource
                    client_sock.sendall(b"ERROR: Resource not found\\n")
                else:
                    # Ungültiges Kommando
                    client_sock.sendall(b"ERROR: Invalid command\\n")

            except Exception as e:
                print(f"Fehler bei Client-Kommunikation: {e}")
            finally:
                client_sock.close()

    except KeyboardInterrupt:
        print("\\nServer wird beendet...")
    finally:
        server_sock.close()


# -------------------- 6. HAUPTPROGRAMM --------------------

if __name__ == "__main__":
    import sys

    print("="*60)
    print("RSA ETP SERVER")
    print("="*60)

    # Generiere Schlüsselpaar
    print("\\nGeneriere RSA Schlüsselpaar (512 Bit)...")
    public_key, private_key = generate_rsa_keypair(512)

    e, n = public_key
    d, _ = private_key

    print(f"\\nÖffentlicher Schlüssel:")
    print(f"  e = {e}")
    print(f"  n = {n:x}")

    # Wähle Port
    port = 12345  # Beispiel-Port

    # Kündige Server an (optional, falls Netzwerk verfügbar)
    # announce_server(port)

    # Starte ETP Server
    print(f"\\nStarte ETP Server auf Port {port}...")
    run_etp_server(port, public_key, private_key)

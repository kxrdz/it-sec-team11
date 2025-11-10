import socket

# Server-Adresse und Port
HOST = '0.0.0.0'
PORT = 12345

def rsa_decrypt(ciphertext, d, n):
    return modpow(ciphertext, d, n)

def modpow(base:int, exponent:int,modulus:int) -> int:
    if modulus == 1:
        return 0
    if exponent < 0:
        raise ValueError("Exponent muss >= 0 sein")
    base %= modulus
    result = 1
    while exponent > 0:
        if exponent & 1:                 # Bit 1? → multiplizieren
            result = (result * base) % modulus
        base = (base * base) % modulus   # Basis quadrieren
        exponent >>= 1                    # Exponent halbieren (Bitshift)
    return result

with open('pubkey', 'r') as f:
    lines = f.readlines()
    e = int(lines[0].split(':')[1].strip())
    e_hex = hex(e)[2:]
    N = int(lines[1].split(':')[1].strip())
    N_hex = format(N, 'x').rjust(128,'0')

with open('privkey', 'r') as f:
    lines = f.readlines()
    d = int(lines[0].split(':')[1].strip())
    N = int(lines[1].split(':')[1].strip())


# Server erstellen
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server läuft auf {HOST}:{PORT}")
    while True:
        # Verbindung akzeptieren
        conn, addr = server.accept()
        with conn:
            print(f"Verbunden mit {addr}")
            while True:
                # Nachricht lesen
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                # wenn der pubkey angefragt wird
                if message.strip() == "GET pubkey ETP/2025":
                    antwort = f"pub: {e_hex}\n N: {N_hex}\n"
                    print("public key send")
                    conn.sendall(antwort.encode())
                else:
                    try:
                        message_int = int(message, 16)
                        ciphertext = rsa_decrypt(message_int, d, N)
                        # <cipher> in bytes umwandeln mit Padding (512 bit)
                        text = ciphertext.to_bytes((ciphertext.bit_length() + 7)//8, "big")
                        # dann die Bytes zu ASCII-Zeichen
                        text_ascii = text.decode()
                        print(text_ascii)
                    except ValueError:
                        # message ist keine gültige hexadezimale Zahl, daher einfach message anzeigen
                        print(message)
import socket

# Server-Adresse und Port
HOST = '0.0.0.0'
PORT = 12345

def rsa_encrypt(message, e, n):
    print("Verschlüsselt eine Nachricht mit RSA")
    return pow(message, e, n)

def rsa_decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

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
                    antwort = f"pub: {e_hex}\nN: {N_hex}\n"
                    print("public key send")
                    conn.sendall(antwort.encode())

                    #nachricht = "Hallo World!"
                    #print(nachricht)
                    #nachricht_bytes = nachricht.encode()
                    #print(nachricht_bytes)
                    #nachricht_int = int.from_bytes(nachricht_bytes, byteorder='big')
                    #print(f"user Nachricht:{nachricht_int}")
                    #antwort = f"\n<<cipher>>{rsa_encrypt(nachricht_int,e,N)}"
                    #conn.sendall(antwort.encode())
                # ansonsten die nachricht enschlüsseln
                else:

                    print(f"nachricht:{message}")
                    ciphertext = rsa_decrypt(int(message), d, N)
                    # <cipher> in byts umwandeln mit padding (512 bit)
                    text = ciphertext.to_bytes((ciphertext.bit_length() + 7)//8, "big" )
                    print(text)
                    # dann die byts zu ascii zeichen
                    text_ascii = text.decode();
                    print(text_ascii)


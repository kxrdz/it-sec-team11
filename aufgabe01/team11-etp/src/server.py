import socket

# Server-Adresse und Port
HOST = '0.0.0.0'
PORT = 12345
PUBKEY = '10001'
NKEY = '65c2f1f2db06b66e9e3e24eb8e1276513ac25c3a5d2b3ff3cf0e91969c0f1172d79824a244f7c74e0effa6a3a6bcfbd7784439de2e1d6059ba978403ebcf4755'
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
                print(f"Nachricht erhalten: {message}")
                if message.strip() == "GET pubkey ETP/2025":
                    with open('pubkey', 'r') as datei:
                        pubkey = datei.read()
                        antwort = f"{pubkey}"
                        print("public key send")
                        conn.sendall(antwort.encode())
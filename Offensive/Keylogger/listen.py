import socket

HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"[+] Listening on {HOST}:{PORT} ...")
conn, addr = server.accept()
print(f"[+] Connected by {addr}\n")

try:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode(), end="")
except KeyboardInterrupt:
    print("\n[!] Server stopped manually.")
finally:
    conn.close()
    server.close()

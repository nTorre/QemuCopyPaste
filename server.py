import socket
import subprocess
import threading
import signal
import sys

HOST = '0.0.0.0'  # Ascolta su tutte le interfacce
PORT = 65432      # Porta per la comunicazione
clipboard = ""
running = True

def set_clipboard(text):
    global clipboard
    clipboard = text
    subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode())
    print(f"Testo copiato negli appunti: {text}")

def get_clipboard():
    return clipboard

def handle_client(conn, addr):
    print(f"Nuova connessione da {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            
            if not data:
                break
            
            print(f"Testo inviato dal client: {data}")
            
            if data.startswith("COPY:"):
                text = data[5:]
                set_clipboard(text)
                print(f"Testo inviato dal client: {text}")

            # elif data == "PASTE":
            #     text = get_clipboard()
            #     conn.sendall(text.encode())
            #     print(f"Testo inviato al client: {text}")
    except Exception as e:
        print(f"Errore nella gestione del client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connessione chiusa con {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server in ascolto su {HOST}:{PORT}")
        
        while running:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
            except Exception as e:
                if running:
                    print(f"Errore nell'accettare la connessione: {e}")

def signal_handler(sig, frame):
    global running
    print("\nChiusura del server...")
    running = False
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    start_server()
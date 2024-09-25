import pyperclip
import socket
from pynput import keyboard
from time import sleep

# Configurazione
HOST = '127.0.0.1'  # Indirizzo IP della macchina virtuale QEMU
PORT = 65432        # Porta per la comunicazione
TIMEOUT = 2         # Timeout per la connessione in secondi

def try_connect():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((HOST, PORT))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def send_to_qemu(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((HOST, PORT))
            s.sendall(message.encode())
            if message.startswith("PASTE"):
                data = s.recv(1024)
                return data.decode()
    except (socket.timeout, ConnectionRefusedError):
        print(f"Impossibile connettersi al server QEMU ({HOST}:{PORT}). Assicurati che il server sia in esecuzione.")
    except Exception as e:
        print(f"Si è verificato un errore durante la comunicazione con QEMU: {e}")
    return None

def on_copy():
    print("Try to send text")
    sleep(0.1)
    text = pyperclip.paste()
    if send_to_qemu(f"COPY:{text}") is not None:
        print(f"Testo inviato a QEMU: {text}")

def main():
    print("Verifica della connessione al server QEMU...")
    if not try_connect():
        print(f"Impossibile connettersi al server QEMU ({HOST}:{PORT}). Assicurati che il server sia in esecuzione.")
        print("Il client continuerà a funzionare, ma le operazioni di copia e incolla potrebbero fallire.")
    else:
        print("Connessione al server QEMU riuscita.")

    print("Client in esecuzione. Usa Ctrl+Shift+C per copiare in QEMU e Ctrl+Shift+V per incollare da QEMU.")
    
    with keyboard.GlobalHotKeys({
            '<cmd>+c': on_copy}) as h:
        h.join()

if __name__ == "__main__":
    main()
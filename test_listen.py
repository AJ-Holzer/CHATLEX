import socket
import time
from env_03.func.Encryption import AES

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 58_000))
    sock.listen(1)

    print("Server is listening for incoming connections...")

    # Establish a connection with a client
    conn, addr = sock.accept()
    print(f"Connected by {addr}")

    # Create an AES encryption object
    aes = AES(b"key")

    # Encrypt and send data to the client
    encrypted_data = aes.encrypt("AJ")
    conn.sendall(encrypted_data)

    # Close the connection
    conn.close()

    time.sleep(4e6)

if __name__ == "__main__":
    main()
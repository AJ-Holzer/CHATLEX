import socket

class Connection:
    def __init__(self, port: int) -> None:
        self.port: int = port
    
    def send(self, message: str) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def recv(self, size: int) -> bytes:
        raise NotImplementedError("This function is not implemented yet!")

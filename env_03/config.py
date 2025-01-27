class Config:
    def __init__(self) -> None:
        # Connection settings
        self.buf_size: int = 1024
        self.port: int = 58_000

        # Encryption settings
        self.encoding: str = 'UTF-8'

        # ChatFile settings
        self.chatfile_path: str = "./chatfile.dat"

config = Config()

class Config:
    def __init__(self) -> None:
        # Window settings
        self.APP_TITLE: str = "OMNI"
        self.APP_TITLE_SEPARATOR: str = " - "
        self.APP_RESIZABLE: bool = False
        self.APP_WIDTH: int = 400
        self.APP_HEIGHT: int = 800
        self.APP_PADDING_TOP = 40

        # Storage settings
        self.CS_USER_PASSWORD_HASH: str = "password-hash"
        self.CS_USER_PASSWORD_IV: str = "password-iv"
        self.SS_USER_SESSION_KEY: str = "session-key"
        self.CS_USER_SALT: str = "salt"

        # Settings for Argon2 key derivation
        self.ARGON2_TIME_COST: int = 40  # Increase for more security (more iterations)
        self.ARGON2_MEMORY_COST: int = 65536  # 64 MB
        self.ARGON2_PARALLELISM: int = 2
        self.ARGON2_HASH_LEN: int = 32  # 256-bit key
        self.SALT_LENGTH: int = 32

        # Routes
        self.ROUTE_CONTACTS: str = "/contacts"
        self.ROUTE_LOGIN: str = "/login"


config = Config()

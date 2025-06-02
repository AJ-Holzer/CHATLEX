class Config:
    # Window settings
    APP_TITLE: str = "ZEPHRA"
    APP_TITLE_SEPARATOR: str = " - "
    APP_RESIZABLE: bool = False
    APP_WIDTH: int = 400
    APP_HEIGHT: int = 800
    APP_PADDING_TOP: int = 40
    APP_PADDING_RIGHT: int = 20
    APP_PADDING_BOTTOM: int = 20
    APP_PADDING_LEFT: int = 20

    # Top bar settings
    TOP_BAR_HEIGHT: int = 50
    TOP_BAR_LABEL_HEIGHT: int = 25
    TOP_BAR_ICON_SIZE: int = TOP_BAR_HEIGHT - 15

    # Storage settings
    CS_USER_PASSWORD_HASH: str = "password-hash"
    CS_USER_PASSWORD_IV: str = "password-iv"
    CS_USER_SALT: str = "salt"
    CS_LOGOUT_ON_LOST_FOCUS: str = "logout-on-lost-focus"
    SS_USER_SESSION_KEY: str = "session-key"

    # Settings for Argon2 key derivation
    ARGON2_TIME_COST: int = 40  # Increase for more security (more iterations)
    ARGON2_MEMORY_COST: int = 65536  # 64 MB
    ARGON2_PARALLELISM: int = 2
    ARGON2_HASH_LEN: int = 32  # 256-bit key
    SALT_LENGTH: int = 32

    # Routes
    ROUTE_CONTACTS: str = "/contacts"
    ROUTE_LOGIN: str = "/login"
    ROUTE_PROFILE: str = "/profile"
    ROUTE_SETTINGS: str = "/settings"

    # Encoding settings
    ENCODING: str = "UTF-8"

    # Encryption settings
    ENCRYPTION_PRIVATE_KEY_FILE: str = "master_key_priv.txt"
    ENCRYPTION_PUBLIC_KEY_FILE: str = "master_key_publ.txt"
    ENCRYPTION_SIGNED_ONION_DATA_FILE: str = "singed_onion_data.json"

    # Database settings
    DATABASE_FILE: str = ""

    # Advanced security settings
    LOGOUT_ON_LOST_FOCUS_DEFAULT: bool = False


config = Config()

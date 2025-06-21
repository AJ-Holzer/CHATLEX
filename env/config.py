from typing import Literal

import flet as ft  # type:ignore[import-untyped]


class Config:
    # Window settings
    APP_TITLE: str = "ChatLex"
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
    CS_PASSWORD_HASH_TIME_COST: str = "pwd-hash-time-cost"
    CS_LOGOUT_ON_LOST_FOCUS: str = "logout-on-lost-focus"
    CS_SHAKE_DETECTION: str = "shake-detection"
    CS_COLOR_SEED: str = "color-seed"
    SS_USER_SESSION_KEY: str = "session-key"

    # Settings for Argon2
    ARGON2_MEMORY_COST: int = 65536  # 64 MB
    ARGON2_PARALLELISM: int = 2
    ARGON2_HASH_LEN: int = 32  # 256-bit key
    ARGON2_MAX_TIME_COST_CALIBRATION: int = 70  # The max time cost for password hashing
    ARGON2_TARGET_PASSWORD_DURATION: float = 0.5  # The duration for password hashing

    # Salt settings
    SALT_LENGTH: int = 32

    # Settings for HKDF
    HKDF_LENGTH: int = 32
    HKDF_INFO_MESSAGE: Literal[b"message-encryption-key"] = b"message-encryption-key"
    HKDF_INFO_CONTACT: Literal[b"contact-encryption-key"] = b"contact-encryption-key"
    HKDF_INFO_DEVICE: Literal[b"device-encryption-key"] = b"device-encryption-key"

    # Routes
    ROUTE_CONTACTS: str = "/contacts"
    ROUTE_LOGIN: str = "/login"
    ROUTE_PROFILE: str = "/profile"
    ROUTE_SETTINGS: str = "/settings"
    ROUTE_CALIBRATIONS: str = "/calibrations"

    # Encoding settings
    ENCODING: str = "UTF-8"

    # Encryption settings
    ENCRYPTION_PRIVATE_KEY_FILE: str = "master_key_priv.txt"
    ENCRYPTION_PUBLIC_KEY_FILE: str = "master_key_publ.txt"
    ENCRYPTION_SIGNED_ONION_DATA_FILE: str = "singed_onion_data.json"

    # Database settings
    DATABASE_FILE: str = "data.db"

    # Advanced security settings
    LOGOUT_ON_LOST_FOCUS_DEFAULT: bool = False

    # Image paths
    APP_LOGO_PNG: str = "assets/icon.png"
    APP_LOGO_ICO: str = "assets/icon.ico"
    APP_LOGO_SPLASH_ANDROID_PNG: str = "assets/splash_android.png"

    # Contact settings
    COLOR_ONLINE: ft.ColorValue = ft.Colors.GREEN
    COLOR_OFFLINE: ft.ColorValue = ft.Colors.RED_400

    # Shake settings (for logout)
    SHAKE_THRESHOLD_GRAVITY: float = (
        2.0  # How strong the phone has to be shaken to trigger logout function
    )
    SHAKE_ENABLED_DEFAULT: bool = True

    # Default appearance settings
    APPEARANCE_COLOR_SEED_DEFAULT: ft.ColorValue = ft.Colors.PURPLE

    # Color picker settings
    COLOR_PICKER_AMOUNT_COLORS: int = (
        16  # The amount of color available in the color picker
    )
    COLOR_PICKER_BUTTON_SIZE: int = 20
    COLOR_PICKER_BUTTON_SPACING: int = 10


config = Config()

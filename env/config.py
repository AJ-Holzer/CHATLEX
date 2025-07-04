from typing import Literal

import flet as ft  # type: ignore[import-untyped]


class Config:
    # Window settings
    APP_TITLE: str = "CHATLEX"
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
    TOP_BAR_LOGOUT_ON_LABEL_CLICK_DEFAULT: bool = True

    # Storage settings
    CS_USER_PASSWORD_HASH: str = "password-hash"
    CS_USER_PASSWORD_IV: str = "password-iv"
    CS_USER_SALT: str = "salt"
    CS_PASSWORD_HASH_TIME_COST: str = "pwd-hash-time-cost"
    CS_LOGOUT_ON_LOST_FOCUS: str = "logout-on-lost-focus"
    CS_SHAKE_DETECTION_ENABLED: str = "shake-detection-enabled"
    CS_COLOR_SEED: str = "color-seed"
    CS_FONT_FAMILY: str = "font"
    CS_FONT_SIZE: str = "font-size"
    CS_SHAKE_DETECTION_THRESHOLD_GRAVITY: str = "shake-detection-threshold-gravity"
    CS_LOGOUT_ON_TOP_BAR_LABEL_CLICK: str = "logout-on-top-bar-label-click"
    CS_LANGUAGE: str = "language"
    SS_USER_SESSION_KEY: str = "session-key"

    # Settings for Argon2
    ARGON2_MEMORY_COST: int = 65536  # 64 MB
    ARGON2_PARALLELISM: int = 2
    ARGON2_HASH_LEN: int = 32  # 256-bit key
    ARGON2_MAX_TIME_COST_CALIBRATION: int = 70  # The max time cost for password hashing
    ARGON2_TARGET_PASSWORD_DURATION: float = 0.5  # The duration for password hashing

    # Salt settings
    SALT_LENGTH: int = 32

    # AES settings
    AES_256_CBC_IV_LENGTH: int = 16
    AES_256_GCM_IV_LENGTH: int = 12

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
    SHAKE_DETECTION_THRESHOLD_GRAVITY_DEFAULT: float = (
        2.0  # How strong the phone has to be shaken to trigger logout function
    )
    SHAKE_DETECTION_THRESHOLD_GRAVITY_MIN: float = 1.3
    SHAKE_DETECTION_THRESHOLD_GRAVITY_MAX: float = 2.5
    SHAKE_DETECTION_ENABLED_DEFAULT: bool = False
    SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER: int = (
        10  # Value needs to be multiplied since the flet slider isn't able to use float for division
    )

    # Default appearance settings
    APPEARANCE_COLOR_SEED_DEFAULT: ft.ColorValue = "#800080"  # Purple
    APPEARANCE_FONT_FAMILY_DEFAULT: str = "varela-round"
    APPEARANCE_FONT_SIZE_DEFAULT: int = 20

    # Color picker settings
    COLOR_PICKER_AMOUNT_COLORS: int = (
        16  # The amount of color available in the color picker
    )
    COLOR_PICKER_BUTTON_SIZE: int = 20
    COLOR_PICKER_BUTTON_SPACING: int = 10

    # Fonts
    # TODO: Only define folder and dynamically load fonts
    FONT_FAMILIES_LOCAL: dict[str, str] = {
        "varela-round": "fonts/varela_round.ttf",
        "baloo-bhaijaan-semibold": "fonts/baloo_bhaijaan_semibold.ttf",
        "baloo-bhaijaan": "fonts/baloo_bhaijaan_regular.ttf",
        "dosis-semibold": "fonts/dosis_semibold.ttf",
    }

    # Font settings
    FONT_SIZE_MIN: int = 10
    FONT_SIZE_MAX: int = 30

    # Files
    FILE_ENCRYPTION_PRIVATE_KEY: str = "master_key_priv.txt"
    FILE_ENCRYPTION_PUBLIC_KEY: str = "master_key_publ.txt"
    FILE_ENCRYPTION_SIGNED_ONION_DATA: str = "singed_onion_data.json"

    # Folder settings
    FOLDER_LANGUAGES: str = "locales"

    # Language settings
    LANGUAGE_NOT_PROVIDED: str = "LANG_NOT_PROVIDED"
    LANGUAGE_NO_STATES_PROVIDED: str = "LANG_STATES_NOT_PROVIDED"
    LANGUAGE_DEFAULT: str = "de"
    LANGUAGE_AVAILABLE_LOCALES: list[str] = ["de", "en"]


config = Config()

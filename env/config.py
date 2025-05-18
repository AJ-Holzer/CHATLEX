import flet as ft  # type:ignore[import-untyped]

class Config:
    def __init__(self) -> None:
        self.FONT_MIN_SIZE           : int            = 15
        self.FONT_MAX_SIZE           : int            = 30
        self.FONT_SIZE_DEFAULT       : int            = 20
        self.FONT_FAMILY_DEFAULT     : str            = "Varela Round"

        # Constants for Argon2 key derivation
        self.ARGON2_TIME_COST        : int            =    40   # Increase for more security (more iterations)
        self.ARGON2_MEMORY_COST      : int            = 65536   # 64 MB
        self.ARGON2_PARALLELISM      : int            =     2
        self.ARGON2_HASH_LEN         : int            =    32   # 256-bit key

        # General colors
        self.COLOR_ONLINE            : ft.ColorValue  = ft.Colors.GREEN
        self.COLOR_OFFLINE           : ft.ColorValue  = ft.Colors.RED_400

        # Chat colors
        self.OTHER_SENDER_COLOR      : ft.ColorValue  = "#5c5c5c"
        self.SELF_SENDER_COLOR       : ft.ColorValue  = ft.Colors.PURPLE_600

        # Client storage keys
        self.CS_FONT_FAMILY          : str            = "font-family"
        self.CS_FONT_SIZE            : str            = "font-size"
        self.CS_PASSWORD_IV          : str            = "password-iv"
        self.CS_PASSWORD_HASH        : str            = "password-hash"
        self.CS_LOGOUT_ON_LOST_FOCUS : str            = "logout-lost-focus"
        
        # Default values
        self.LOGOUT_ON_LOST_FOCUS_DEFAULT    : bool           = False

config = Config()

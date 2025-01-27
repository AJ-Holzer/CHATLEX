class Config:
    def __init__(self) -> None:
        # DB settings
        self.db_name: str = "messages.sqlite3"

config = Config()
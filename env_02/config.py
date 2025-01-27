class Config:
    def __init__(self) -> None:
        # DB settings
        self.db_name: str = "Test_02.sqlite3"
        self.create_messages: str = "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, timestamp FLOAT, content TEXT, sent BOOLEAN)"
        self.create_users: str = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, timestamp FLOAT, username TEXT, address TEXT, port INTEGER)"

config = Config()

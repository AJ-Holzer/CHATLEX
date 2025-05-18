# import sqlite3

# # Use pysqlcipher3 instead if installed
# from pysqlcipher3 import dbapi2 as sqlcipher  # type:ignore

# conn = sqlcipher.connect('')

# # Set the key
# conn.execute("PRAGMA key = 'your-strong-password'")

# # Optional: to verify encryption is working
# conn.execute("PRAGMA cipher_version;")
# print(conn.fetchone())

# # Now you can use it like normal sqlite3
# conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, msg TEXT);")
# conn.execute("INSERT INTO test (msg) VALUES (?)", ("Hello Secure World!",))
# conn.commit()

# conn.close()

import sqlite3

# connect to database
conn = sqlite3.connect("../data/Chinook.db")
cursor = conn.cursor()

# get tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

# get schema of a table
cursor.execute("PRAGMA table_info(albums);")
schema = cursor.fetchall()
print("Schema of the table:")
for column in schema:
    print(column)

# close database
conn.close()

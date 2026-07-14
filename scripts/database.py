import sqlite3
conn = sqlite3.connect("retail.db")
with open("sql/schema.sql", "r") as file:
    schema = file.read()
conn.executescript(schema)

print("Database and tables created successfully!")

conn.close()

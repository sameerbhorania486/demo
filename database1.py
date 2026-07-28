import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor() # ye ek pointer hai jo SQL commands execute karta hai

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
)
""")

print("Table Created Successfully...")
conn.commit() #changes ko permanently save karta hai database mai
conn.close()
import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, role TEXT, password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, genre TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, book_id INTEGER, rating INTEGER, comment TEXT)")

conn.commit()
conn.close()

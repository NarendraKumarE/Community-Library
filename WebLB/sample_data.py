import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

admin = ('Admin', 'admin@library.com', 'admin', 'admin123')
user = ('User1', 'user1@lib.com', 'member', 'user123')
book1 = ('1984', 'George Orwell', 'Dystopian')
book2 = ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy')

cur.execute("INSERT OR IGNORE INTO users (name, email, role, password) VALUES (?, ?, ?, ?)", admin)
cur.execute("INSERT OR IGNORE INTO users (name, email, role, password) VALUES (?, ?, ?, ?)", user)

cur.execute("INSERT OR IGNORE INTO books (title, author, genre) VALUES (?, ?, ?)", book1)
cur.execute("INSERT OR IGNORE INTO books (title, author, genre) VALUES (?, ?, ?)", book2)

conn.commit()

# Check insert success
users = cur.execute("SELECT * FROM users").fetchall()
books = cur.execute("SELECT * FROM books").fetchall()

print("[INFO] Sample data added.")
print(f"[INFO] Total users: {len(users)}")
print(f"[INFO] Total books: {len(books)}")

conn.close()

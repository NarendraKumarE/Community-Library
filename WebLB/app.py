from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from utils.fines import calculate_fine
from utils.qr_code import generate_qr

app = Flask(__name__)
app.secret_key = 'library_secret'

def get_db():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, pwd)).fetchone()
        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["name"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] == "admin":
        return render_template("dashboard_admin.html", name=session["name"])
    return render_template("dashboard_member.html", name=session["name"])

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO users (name, email, role, password) VALUES (?, ?, ?, ?)", (
            request.form["name"], request.form["email"], request.form["role"], request.form["password"]
        ))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_user.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO books (title, author, genre) VALUES (?, ?, ?)", (
            request.form["title"], request.form["author"], request.form["genre"]
        ))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_book.html")

@app.route("/books")
def list_books():
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("list_books.html", books=books)

@app.route("/users")
def list_users():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    db = get_db()
    users = db.execute("SELECT id, name, email, role FROM users").fetchall()
    return render_template("list_users.html", users=users)

@app.route("/reserve", methods=["GET", "POST"])
def reserve():
    db = get_db()
    books = db.execute("SELECT * FROM books WHERE id NOT IN (SELECT book_id FROM reservations)").fetchall()
    if request.method == "POST":
        db.execute("INSERT INTO reservations (user_id, book_id) VALUES (?, ?)", (
            session["user_id"], request.form["book_id"]
        ))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("reserve.html", books=books)

@app.route("/reservations")
def view_reservations():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    db = get_db()
    reservations = db.execute("""
        SELECT reservations.id AS res_id, users.name AS user_name, books.title AS book_title
        FROM reservations
        JOIN users ON reservations.user_id = users.id
        JOIN books ON reservations.book_id = books.id
    """).fetchall()
    return render_template("reservations.html", reservations=reservations)

@app.route("/remove_reservation/<int:res_id>")
def remove_reservation(res_id):
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    db = get_db()
    db.execute("DELETE FROM reservations WHERE id = ?", (res_id,))
    db.commit()
    return redirect(url_for("view_reservations"))

@app.route("/review", methods=["GET", "POST"])
def review():
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    if request.method == "POST":
        db.execute("INSERT INTO reviews (book_id, rating, comment) VALUES (?, ?, ?)", (
            request.form["book_id"], request.form["rating"], request.form["comment"]
        ))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("review.html", books=books)

@app.route("/reviews")
def view_reviews():
    db = get_db()
    reviews = db.execute("""
        SELECT books.title AS book_title, reviews.rating, reviews.comment
        FROM reviews
        JOIN books ON reviews.book_id = books.id
        ORDER BY book_title
    """).fetchall()
    return render_template("reviews.html", reviews=reviews)

@app.route("/fine", methods=["GET", "POST"])
def fine():
    fine = None
    error = None
    if request.method == "POST":
        issue_date = request.form.get("issue")
        return_date = request.form.get("return")
        if issue_date and return_date:
            try:
                fine = calculate_fine(issue_date, return_date)
            except Exception as e:
                error = f"Error calculating fine: {e}"
        else:
            error = "Both dates are required."
    return render_template("fine.html", fine=fine, error=error)
@app.route("/")
def home():
    return render_template("home.html")



@app.route("/qr", methods=["GET", "POST"])
def qr():
    qr_path = None
    if request.method == "POST":
        qr_path = generate_qr(request.form["book_id"])
    return render_template("qr_result.html", qr_path=qr_path)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

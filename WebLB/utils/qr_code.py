import qrcode
import os

def generate_qr(book_id):
    os.makedirs("static/qr_codes", exist_ok=True)
    path = f"static/qr_codes/book_{book_id}.png"
    qrcode.make(f"Book ID: {book_id}").save(path)
    return path

from flask import Flask, request, redirect, url_for, send_file, render_template, session
import os, uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change this in real use

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Login credentials
USERNAME = "admin"
PASSWORD = "1234"

# Store files as {id: filepath}
file_db = {}

@app.route("/")
def home():
    return render_template("index.html", logged_in=session.get("logged_in", False))

@app.route("/login", methods=["POST"])
def login():
    if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
        session["logged_in"] = True
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("logged_in"):
        return redirect(url_for("home"))
    file = request.files["file"]
    if file:
        file_id = str(uuid.uuid4().int)[:6]  # generate short unique ID
        filepath = os.path.join(UPLOAD_FOLDER, f"{file_id}_{file.filename}")
        file.save(filepath)
        file_db[file_id] = filepath
        return f"<h3>✅ File uploaded! Your File ID: #{file_id}</h3><a href='/'>Back</a>"
    return "❌ Upload failed"

@app.route("/download", methods=["POST"])
def download():
    file_id = request.form["file_id"].replace("#", "")
    if file_id in file_db:
        return send_file(file_db[file_id], as_attachment=True)
    return "❌ File not found"

if __name__ == "__main__":
    app.run(debug=True)

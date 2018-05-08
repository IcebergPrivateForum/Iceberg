from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import database

app = Flask(__name__)
app.secret_key = "Mo1 s3Cr3T Ki K4Y?"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'

@login_manager.user_loader
def load_user(userid):
    try:
        return database.User.get(id=userid)
    except database.DoesNotExist:
        return None

@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    name = request.args.get('name', '').title()
    if name:
        user = database.User.get(name=name)
        if check_password_hash(user.passcode, request.args.get("passcode", "")):
            login_user(user)
            return redirect(url_for('forum'))
    return render_template("home.html")

@app.route('/forum')
@login_required
def forum():
    message = request.args.get("message", "")
    message_too_long = False
    if message:
        if len(message) > 125:
            message_too_long = True
        else:
            database.post_message(message, current_user.name)
    messages = database.retrieve_messages()
    return render_template("forum.html", messages=messages, message_too_long=message_too_long)

@app.route('/register')
def register():
    name, password = request.args.get("name", ""), request.args.get("password", "")
    passcode = request.args.get("passcode", "")
    role = request.args.get("role", "")
    if passcode == "tophat":
        if name and password and role:
            database.User.secure_create(name=name, passcode=password, role=role)
            user = database.User.get(name=name)
            login_user(user)
            return redirect(url_for('forum'))
    return render_template("register.html")

app.run(debug=True, port=5173)
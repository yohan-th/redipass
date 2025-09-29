import os, secrets
from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.tools import track_sending, track_loading

CORRECT_PASSWORD = os.getenv("PASSWORD")
URL_REDIRECT = os.getenv("URL_REDIRECT")

# --- CONFIGURATION ---
app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(64)
csrf = CSRFProtect(app)

# --- RATE LIMITER ---
limiter = Limiter(key_func=get_remote_address, default_limits=["10 per hour"])
limiter.init_app(app)

# --- FORM CLASS ---
class LoginForm(FlaskForm):
    password = PasswordField("", validators=[DataRequired()])
    submit = SubmitField("Verify")

# --- ROUTES ---
@app.errorhandler(429)
def ratelimit_error(e):
    return render_template("too_many_request.html"), 429

@app.route("/", methods=["GET", "POST"])
def login():
    track_loading(request)
    form = LoginForm()
    if form.validate_on_submit():  # Handles CSRF and method==POST
        track_sending(request)
        if form.password.data == CORRECT_PASSWORD:
            return redirect(URL_REDIRECT)
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(port=8080)

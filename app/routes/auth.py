from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user

from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import db, bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.home"))

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():

    print("LOGIN ROUTE REACHED")

    form = LoginForm()

    print("REQUEST METHOD:", request.method)

    if form.validate_on_submit():

        print("FORM VALIDATED")

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        print("EMAIL ENTERED:", form.email.data)
        print("USER FOUND:", user)

        if user:

            password_match = bcrypt.check_password_hash(
                user.password,
                form.password.data
            )

            print("PASSWORD MATCH:", password_match)

            if password_match:
                login_user(user)
                return redirect(url_for("main.home"))

    else:
        print("FORM ERRORS:", form.errors)

    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("main.home"))
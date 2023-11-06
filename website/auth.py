from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Successfully logged-in", category='success')
                login_user(user, remember=True )
                return redirect(url_for("front.home"))
            else :
                flash("Incorrcet password", category='success')
        else :
            flash("User dosent exist", category='error')

    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(firstName=firstName).first()

        if user_exists:
            flash("User already exist with this email", category="error")
        elif username_exists:
            flash("username alraedy taken", category='error')
        elif len(email) < 7:
            flash("Email must be greater then 6 characters", category='error')
        elif len(firstName) < 4:
            flash("Name should at least have 4 characters", category='error')
        elif password1 != password2:
            flash("Passwords don\'t match!", category='error')
        elif len(password1) < 5:
            flash("Password should at least have 5 characters", category='error')
        else :
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='Sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Accound Registerd", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for("front.home"))

    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
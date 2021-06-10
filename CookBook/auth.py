from flask import Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .model.User import User
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .app import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login SuccessFul')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash("Incorrect Password, Please try again", category='error')
        else:
            flash("email is not valid", category="error")
    else:
        return render_template("login.html", user=current_user)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists please try another one.")
        elif len(username) < 4:
            flash("Username needs to be greater than 3 characters.")
        elif len(password) < 7:
            flash("Password needs to be greater than 6 characters.")
        else:
            newUser = User(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(
                password, method='sha256'),username=username)
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash('Account created!', category='success')
            return render_template("dashboard.html", user=current_user)
    return render_template("signup.html", user=current_user)

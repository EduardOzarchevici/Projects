from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, logout_user, login_user

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login succefull', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: flash('Wrong password', category='error')
        else: flash('User does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use', category='error')
        elif len(email) < 3 :
            flash('Email needs to be at least 3 characters long', category='error')
        elif len(name) < 1:
            flash('Name needs to be at least 1 character long', category='error')
        elif password1 != password2:
            flash('Passwords are not the same', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characthers long', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))


    return render_template('sign_in.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


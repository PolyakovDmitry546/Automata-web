from flask import Blueprint, render_template, flash, redirect, url_for, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

from models import User
from forms import LoginForm, RegisterFrom
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(login=login).first()

        if not user or not check_password_hash(user.password, password):
            flash('Неверный логин или пароль.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)

@auth.route('/try_login', methods=['POST'])
def get_id():
    if request.form.get('login') and request.form.get('password'):
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login).first()

        if not user or not check_password_hash(user.password, password):
            return "None"

        return str(user.id)
    
    return "None"

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = RegisterFrom()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data

        user = User.query.filter_by(login=login).first()

        if user:
            flash('Логин уже существует.')
            return redirect(url_for('auth.signin'))

        new_user = User(login=login, name=name, surname=surname,
         password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
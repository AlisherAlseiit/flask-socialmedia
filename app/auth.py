from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import RegisterForm, LoginForm
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, url_prefix='/')

@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        passw=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account created successfully! You are now logged in as {new_user.username}", category='success')
        login_user(new_user)
        return redirect(url_for('views.home_page')) 
    if form.errors != {}: #If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template("register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Success! You are logged in as: {user.username}', category='success')
            return redirect(url_for('views.posts_page')) 
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("views.home_page"))
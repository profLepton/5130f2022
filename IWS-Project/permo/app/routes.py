from email.errors import FirstHeaderLineIsContinuationDefect
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, Config
from app.forms import LoginForm, ProfessorRegistrationForm, StudentRegistrationForm, EditProfileForm, ResetPasswordForm
from app.models import User
from datetime import datetime
from app.forms import ResetPasswordRequestForm
from app.emails import send_password_reset_email


@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html', title='Home' )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
        firstName=form.firstName.data, lastName=form.lastName.data, is_professor=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered student!')
        return redirect(url_for('login'))
    return render_template('register_student.html', title='Register', form=form)

@app.route('/register_professor', methods=['GET', 'POST'])
def register_professor():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ProfessorRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
        firstName=form.firstName.data, lastName=form.lastName.data, is_professor=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user, Professor!')
        return redirect(url_for('login'))
    return render_template('register_professor.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts = posts)

#Runs before every request.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.about_me.data = current_user.about_me
        form.location.data = current_user.location
    return render_template('edit_profile.html', title='Edit Profile', form = form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
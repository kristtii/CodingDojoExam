from flask_app import app

from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.show import Show

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/shows')
    return redirect('/logout')


@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if not user:
        flash('This email does not exist.', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/')


@app.route('/registerPage')
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')

    if User.get_user_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)

    if not User.validate_user(request.form):
        return redirect(request.referrer)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'confirm_password': request.form['confirm_password']
    }
    User.create_user(data)
    flash('User succefully created', 'userRegister')
    return redirect('/')


@app.route('/shows')
def shows():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(loggedUserData)
    likesShows = User.getUserLikedShows(loggedUserData)
    if not loggedUser:
        return redirect('/logout')
    return render_template('shows.html', loggedUser=User.get_user_by_id(loggedUserData), shows=Show.get_all(), likesShows=likesShows)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')

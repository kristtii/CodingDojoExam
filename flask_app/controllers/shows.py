from flask_app import app

from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.show import Show


@app.route('/add/show')
def addPost():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    return render_template('addShow.html', loggedUser=User.get_user_by_id(loggedUserData))


@app.route('/create/show', methods=['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validate_show(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Show.create_show(data)
    return redirect('/')


@app.route('/shows/<int:id>')
def viewshow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'show_id': id
    }
    loggedUser = User.get_user_by_id(data)
    show = Show.get_show_by_id(data)
    creator = Show.showCreator(data)
    likes = Show.getShowLikes(data)
    return render_template('show.html', show=show, loggedUser=loggedUser, creator=creator, likes=likes)


@app.route('/shows/edit/<int:id>')
def editshow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'show_id': id
    }
    loggedUser = User.get_user_by_id(data)
    show = Show.get_show_by_id(data)
    if loggedUser['id'] == show['user_id']:
        return render_template('editshow.html', show=show, loggedUser=loggedUser)
    return redirect(request.referrer)


@app.route('/shows/delete/<int:id>')
def deletePost(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'show_id': id
    }
    loggedUser = User.get_user_by_id(data)
    show = Show.get_show_by_id(data)
    if loggedUser['id'] == show['user_id']:
        Show.delete_show_likes(data)
        Show.delete_show(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/edit/show/<int:id>', methods=['POST'])
def updateshow(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validate_show(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'user_id': session['user_id'],
        'show_id': id
    }
    loggedUser = User.get_user_by_id(data)
    show = Show.get_show_by_id(data)
    if loggedUser['id'] == show['user_id']:
        Show.update_show(data)
        flash('Update succesfull!', 'updateDone')
        return redirect('/')
    return redirect('/')


@app.route('/like/<int:id>')
def like(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'show_id': id
    }
    usersWhoLikesThisshow = Show.getUserWhoLikedshows(data)
    if session['user_id'] not in usersWhoLikesThisshow:
        Show.like(data)
    return redirect(request.referrer)


@app.route('/unlike/<int:id>')
def unlike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'show_id': id
    }
    usersWhoLikesThisshow = Show.getUserWhoLikedshows(data)
    if session['user_id'] in usersWhoLikesThisshow:
        Show.unlike(data)
    return redirect(request.referrer)

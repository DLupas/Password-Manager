from app import app, db
from app.models import User
from flask import render_template, url_for, redirect, request
from flask_login import current_user, login_required, login_user, logout_user

@app.route('/')
@app.route('/index') #Homepage
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST']) #login page
def login():
    if request.form.get('username'): #If there is a returned html form
        user = User.query.filter_by(username=request.form['username']).first() #query database for specific user
        password = request.form['password'] #return password
        if user is None or not user.check_pass(password): #checks if there is a user and if the password is correct
            return redirect('/login') #If incorrect, redirect back to login page
        else:
            login_user(user) #Login user and send them to the vault
            return redirect('/')
            '''next = flask.request.args.get('next')
            if not is_safe_url('next'):
                return flask.abort(400)
            return redirect('next' or '/') '''
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST']) #Sign Up Page
def signup(): 
    if request.form.get('username'):
        db.create_all() #creates database
        user = User(username=request.form['username']) #creates object of class User with attribute username
        user.set_pass(request.form['password']) #Hashes password
        db.session.add(user)
        db.session.commit() #Adds user to database
        return redirect('/')
    return render_template('signup.html') #else sends user to signup page

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/vault', methods=['GET', 'POST'])
@login_required
def vault():
    return render_template('vault.html', user=current_user.username)


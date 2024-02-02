from flask import render_template, url_for, flash, redirect
from flask_login import login_user,current_user, logout_user
from Restaurant import app,db
from Restaurant.model import User
from Restaurant.form import RegistrationForm, LoginForm
@app.route("/")
@app.route("/Main Page")
def home(us='Sign/Log In'):
    return render_template('index.html',title='Home',us=us)


@app.route("/Specials")
def special():
    return render_template('special.html',title='Special',us='Sign/Log In')

@app.route("/menu")
def menu():
    return render_template('menu.html',title='Menu',us='Sign/Log In' )



@app.route("/login", methods=['GET', 'POST'])
def registerlog():
    if current_user.is_authenticated:
         redirect (url_for ('home'))

    regform = RegistrationForm()
    logform = LoginForm()
    if regform.validate_on_submit():
        user = User(username=regform.username.data, email=regform.email.data, password=regform.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {regform.username.data}!', 'success')
        login_user(user, remember=regform. remember .data)

      
        return redirect(url_for('home'))
    elif logform.validate_on_submit():
        user = User.query.filter_by(email=logform.email.data).first()
        if user and user.password==logform.password.data :
            flash('You have been logged in!', 'success')
            login_user(user, remember=logform. remember .data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Sign Up/Login', regform=regform,logform=logform,us='Sign/Log In')
@app. route ("/logout")
def logout():
  logout_user ()
  redirect (url_for('home'))

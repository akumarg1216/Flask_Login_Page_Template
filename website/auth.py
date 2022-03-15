from flask import Blueprint, flash, render_template, request, flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_required,logout_user,login_user,current_user

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        city = request.form.get("city")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("E-mail already registered. Login to go to your account.",category='error')

        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category='error')
        elif(len(firstname) < 2):
            flash("First Name must be greater than 1 character", category='error')
        elif(len(password1) < 7):
            flash("Password must be greater than 7 characters.", category='error')
        elif(password1 != password2):
            flash("Passwords don't match", category='error')
        elif(len(city)==0):
            flash("Kindly enter your city name",category='error')
        else:
            new_user = User(email=email, first_name=firstname, last_name=lastname, city=city, password = generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Thanks for registering.", category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html",user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Welcome Back. Login Successful", category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Wrong Password. Kindly try again", category='error')
        else:
            flash('E-mail is not registered. Signup to enjoy our services.',category='error') 

    return render_template('login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
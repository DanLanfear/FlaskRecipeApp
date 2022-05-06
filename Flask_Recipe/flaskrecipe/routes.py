from flask import render_template, url_for, flash, redirect, request
from flaskrecipe.models import User, Recipe, Ingredient, Step
from flaskrecipe.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskrecipe import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

recipes = [
    {
        'author': 'Dan',
        'title': 'Chicken',
        'time': 10,
        'ingredients': [
            'chicken', 
            'pam'
        ],
        'steps': [
            'turn on grill',
            'spray pam on chicken',
            'cook chicken for 7 minutes'
        ],
        'date_posted': 'April 20, 2018',
        'rating': 4,
        'favorite': True
    },
    {
        'author': 'Gab',
        'title': 'Beef',
        'time': 15,
        'ingredients': [
            'beef', 
            'cheese'
        ],
        'steps': [
            'ground the beef',
            'cover in cheese',
            'cook over an open fire'
        ],
        'date_posted': 'April 22, 2018',
        'rating': 5,
        'favorite': False
    }
]


@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html', recipes=recipes)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

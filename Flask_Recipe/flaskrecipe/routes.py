from flask import render_template, url_for, flash, redirect
from flaskrecipe.models import User, Recipe, Ingredient, Step
from flaskrecipe.forms import RegistrationForm, LoginForm
from flaskrecipe import app


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You\'ve been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

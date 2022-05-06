from turtle import title
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '76cfc85495c7ebcab796bb35e32926b8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    steps = db.relationship('Step', backref='recipe', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Recipe('{self.title}', '{self.date_posted}')"


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    step = db.Column(db.Text, nullable=False)
    

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return f"Ingredient('{self.ingredient}', '{self.quantity} {self.label}')"


recipes = [
    {
        'author': 'Dan',
        'title': 'Chicken',
        'prep_time': 10,
        'cook_time': 7,
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
        'title': 'Not Chicken',
        'prep_time': 15,
        'cook_time': 20,
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

if __name__ == '__main__':
    app.run(debug=True)
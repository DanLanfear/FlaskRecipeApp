from flaskrecipe import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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
    category = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    steps = db.relationship('Step', backref='recipe', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Recipe('{self.title}', '{self.description}')"


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    step = db.Column(db.Text, nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Step('{self.step_number}', '{self.step}')"
    

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quantity_label = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return f"Ingredient('{self.ingredient}', '{self.quantity} {self.quantity_label}')"

from flask import render_template, url_for, flash, redirect, request
from flaskrecipe.models import User, Recipe, Ingredient, Step
from flaskrecipe.forms import RecipeForm, RegistrationForm, LoginForm, UpdateAccountForm, IngredientForm, StepForm
from flaskrecipe import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home")
@app.route("/")
def home():
    recipes = Recipe.query.all()
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


@app.route("/recipe/new", methods=['GET','POST'])
@login_required
def new_recippe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, time=form.time.data, description = form.description.data, author=current_user)
        db.session.add(recipe)
        db.session.commit()
        for field in form.ingredients:
            ingredient = Ingredient(ingredient=field.ingredient.data, quantity=field.quantity.data, 
                                    quantity_label=field.quantity_label.data, recipe=Recipe.query.filter_by(title=recipe.title).first())
            db.session.add(ingredient)
        num = 1
        for field in form.steps:
            step = Step(step=field.step.data, step_number=num, recipe=Recipe.query.filter_by(title=recipe.title).first())
            db.session.add(step)
            num += 1
        db.session.commit()
        flash('Recipe submitted', 'success')
        return redirect(url_for('home'))
    return render_template('create_recipe.html', title='New Recipe', form=form)
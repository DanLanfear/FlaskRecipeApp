from flask import Flask, render_template
app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)
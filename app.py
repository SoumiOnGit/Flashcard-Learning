from flask import Flask , render_template , request , redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

    
class User(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        username = db.Column(db.String(200), nullable = False)
        email = db.Column(db.String(200), nullable = False)
        password = db.Column(db.String(200), nullable = False)
        user_decks = relationship('Deck', backref='user_owner', lazy=True)

    
        def __repr__(self):
            return '<User %r>' % self.username

class Deck(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_score = db.Column(db.Integer, nullable = False)
        cards = relationship('Card', backref='deck', lazy=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        deck_user = relationship('User', backref='decks_owned', lazy=True)

class Card(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        front = db.Column(db.String(200), nullable = False)
        back = db.Column(db.String(200), nullable = False)
        card_score = db.Column(db.Integer, nullable = False , default = 0)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False) 
        card_deck = relationship('Deck', backref='cards_in_deck', lazy=True)



if not os.path.exists("./test.db"):
    with app.app_context():
            db.create_all()
            

@app.route('/signup',methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username,email=email,password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding new user'

    return render_template('signup.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        users=User.query.all()
        for user in users:
            if user.email == email and user.password == password :
                print("inside if condition")
                return redirect(f'/user_dashboard/{user.id}')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/user_dashboard/<int:user_id>', methods=['GET'])
def user_dashboard(user_id):
     user = User.query.get_or_404(user_id)
     return render_template('user_dashboard.html', user = user)


if __name__ == '__main__':
    
    app.run(debug=True)


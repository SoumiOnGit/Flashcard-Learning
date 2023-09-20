from flask import Flask , render_template
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
        user_decks = relationship('Deck', backref='user', lazy=True)
    
        def __repr__(self):
            return '<User %r>' % self.username

class Deck(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_score = db.Column(db.Integer, nullable = False)
        cards = relationship('Card', backref='deck', lazy=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        user = relationship('User', backref='decks', lazy=True)

class Card(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        front = db.Column(db.String(200), nullable = False)
        back = db.Column(db.String(200), nullable = False)
        card_score = db.Column(db.Integer, nullable = False , default = 0)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False) 
        card_deck = relationship('Deck', backref='cards', lazy=True)



if not os.path.exists("./test.db"):
    with app.app_context():
            db.create_all()
            


if __name__ == '__main__':
    
    app.run(debug=True)


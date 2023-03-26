from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from base64 import b64encode


app = Flask(__name__)
app.config['SECRET_KEY'] = b64encode(urandom(24)).decode('utf-8')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oneliners.db'
db = SQLAlchemy(app)

class Oneliner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        content = request.form['content']
        link = request.form['link']
        email = request.form['email']
        oneliner = Oneliner(content=content, link=link, email=email)
        db.session.add(oneliner)
        db.session.commit()
        flash('Your one-liner will be sent to ' + email)
    return render_template('home.html')

if __name__ == '__main__':
    import secrets
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)

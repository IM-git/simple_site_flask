from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/', methods=('POST', 'GET'))
def index():
    if request.method == 'POST':
        try:
            text = Text(text=request.form['text'])
            db.session.add(text)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print('Error added in DB.')
    info = []
    try:
        info = Text.query.all()
    except:
        print('Error reading on DB.')
    return render_template('index.html', list=info)

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))

    def __repr__(self):
        return f"<Text {self.id}>"

if __name__ == "__main__":
    app.run(debug=True)
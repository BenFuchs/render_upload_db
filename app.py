from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Relative path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/", methods=['POST'])
def addUser():
    data = request.get_json()
    username=data.get("username")
    email=data.get('email')

    newUser = User(username=username, email=email)
    db.session.add(newUser)
    db.session.commit()
    return "user added"

@app.route("/showuser")
def showUser():
    user_list=db.session.query(User).all()
    user = [{
        "username": user.username,
        "email": user.email
    }for user in user_list]
    return jsonify(user)



if __name__ == '__main__':
    if not os.path.exists('test.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

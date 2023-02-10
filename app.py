from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)
#Creates a flask application instance and assigns it to the variable flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Sets configuration for SQLAlchemy specifying database URI
db = SQLAlchemy(app)
#Creates and instance of SQAlchemy and assigns it to db and this is used to interact with the database. 
app.config['SECRET_KEY'] = 'thisisasecretkey'
# This is a secret key for the flask    




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm():
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})



class LoginForm():
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
@app.route('/')
def home():
    return render_template('home.html')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()


if __name__ == "__main__":
    app.run(debug=True)
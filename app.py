from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__) 
#Creates a flask application instance and assigns it to the variable flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
# Sets configuration for SQLAlchemy specifying database URI 
bcrypt = Bcrypt(app)
# hashed-passwords
db = SQLAlchemy(app) #Creates and instance of SQAlchemy and assigns it to db and this is used to interact with the database. app.config['SECRET_KEY'] = 'thisisasecretkey' # This is a secret key for the flask
app.config['SECRET_KEY'] = 'thisisasecretkey'
#secret key for the flask

login_manager = LoginManager()
# This line creates an instance of the LoginManager class from the flask_login library
login_manager.init_app(app)
# This line initializes the LoginManager instance with your Flask application, app. 
# This is required in order to use the functionality provided by flask_login.


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# The load_user function takes a single argument user_id which is the user's identifier.
# The function returns a user object obtained by querying the User model for the user with the specified user_id. 
# The user object is then stored in the current session,  allowing the application to keep track of the user's identity and state between requests.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
#used to store user information in the database
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')


    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'The username already exists. Please choose a different username.')
#This checks if there is already a username in the database and if there is it asks the user to choose a different username

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')
# Link to home page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)
# Uses bycrypt to hash password

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
# This redirects to dashboard page ones loged in, and log in succesful is required.

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# Logout and redirects you back to log in

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
# hashes the password to keep it secure and then it adds it to the database. 

if __name__ == "__main__":
    app.run(debug=True)
# Enables flask debug mode




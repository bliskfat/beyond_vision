from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
#from sklearn.metrics import precision_score, recall_score, f1_score
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback
#from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
import json

from models import TrainingResult

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = 'your_secret_key'
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@app.route("/presentation")
def presentation():
    return render_template('presentation.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('presentation'))

@app.route("/")
@login_required
def index():
    return render_template('index.html')

@app.route("/basics")
@login_required
def basics():
    return render_template('basics.html')

@app.route("/training")
@login_required
def training():
    return render_template('training.html')

@app.route("/examples")
@login_required
def examples():
    return render_template('examples.html')

@app.route("/contact")
@login_required
def contact():
    return render_template('contact.html')

class TrainingProgress(Callback):
    def __init__(self):
        self.progress = []
        self.losses = []
        self.accuracies = []
        self.precisions = []
        self.recalls = []
        self.f1_scores = []
        self.val_data = None

    def on_epoch_end(self, epoch, logs=None):
        self.progress.append((epoch, logs['loss'], logs['accuracy']))
        self.losses.append(logs['loss'])
        self.accuracies.append(logs['accuracy'])
        if self.validation_data:
            self.val_data = self.validation_data
            y_pred = (self.model.predict(self.val_data[0]) > 0.5).astype(int)
            y_true = self.val_data[1]
            self.precisions.append(precision_score(y_true, y_pred))
            self.recalls.append(recall_score(y_true, y_pred))
            self.f1_scores.append(f1_score(y_true, y_pred))

    def on_train_end(self, logs=None):
        # Calculate additional metrics at the end of training
        if self.val_data:
            y_pred = (self.model.predict(self.val_data[0]) > 0.5).astype(int)
            y_true = self.val_data[1]
            self.precisions.append(precision_score(y_true, y_pred))
            self.recalls.append(recall_score(y_true, y_pred))
            self.f1_scores.append(f1_score(y_true, y_pred))


@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    epochs = int(data['epochs'])
    learning_rate = float(data['learning_rate'])
    layers = int(data['layers'])
    neurons = int(data['neurons'])

    # Generate dummy data
    X = np.random.rand(1000, 1)
    y = (2 * X + 1 + np.random.normal(0, 0.1, (1000, 1)) > 2.5).astype(int)  # Binary classification

    # Build the model
    model = Sequential()
    model.add(Dense(neurons, input_dim=1, activation='relu'))
    for _ in range(layers - 1):
        model.add(Dense(neurons, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='binary_crossentropy', metrics=['accuracy'])

    # Initialize the callback to track progress
    progress_callback = TrainingProgress()

    # Train the model
    model.fit(X, y, epochs=epochs, verbose=0, validation_split=0.2, callbacks=[progress_callback])

    # Return the training loss and accuracy
    return jsonify({
        'loss': progress_callback.losses,
        'accuracy': progress_callback.accuracies,
        'precision': progress_callback.precisions,
        'recall': progress_callback.recalls,
        'f1_score': progress_callback.f1_scores,
        'progress': progress_callback.progress,
        'config': {
            'epochs': epochs,
            'learning_rate': learning_rate,
            'layers': layers,
            'neurons': neurons
        }
    })
@app.route('/results', methods=['GET'])
@login_required
def view_results():
    results = TrainingResult.query.filter_by(user_id=current_user.id).all()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

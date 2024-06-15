from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback
from datetime import datetime
import numpy as np
import json
from forms import RegistrationForm, LoginForm
from models import db, User, TrainingResult

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = 'your_secret_key'
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    return render_template('training_test.html')

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

    def on_epoch_end(self, epoch, logs=None):
        self.progress.append((epoch, logs['loss'], logs['accuracy']))
        self.losses.append(logs['loss'])
        self.accuracies.append(logs['accuracy'])

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
    model.fit(X, y, epochs=epochs, verbose=0, callbacks=[progress_callback])

    # Save the training result to the database
    result = TrainingResult(
        user_id=current_user.id,
        epochs=epochs,
        learning_rate=learning_rate,
        layers=layers,
        neurons=neurons,
        loss=json.dumps(progress_callback.losses),
        accuracy=json.dumps(progress_callback.accuracies)
    )
    db.session.add(result)
    db.session.commit()

    # Return the training loss and accuracy
    return jsonify({
        'loss': progress_callback.losses,
        'accuracy': progress_callback.accuracies,
        'progress': progress_callback.progress
    })

@app.route('/results', methods=['GET'])
@login_required
def results():
    results = TrainingResult.query.filter_by(user_id=current_user.id).all()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

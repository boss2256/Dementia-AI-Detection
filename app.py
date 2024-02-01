from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import json

import os
from keras.models import load_model
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    cognitive_tests = db.relationship('CognitiveTestData', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




# Load your trained model (replace 'best_model.h5' with your model's file path)
model_path = os.path.join(os.path.dirname(__file__), 'models', 'tuned_model.h5')
model = load_model(model_path)

@app.route('/predict', methods=['POST'])
@login_required  # Add appropriate authentication/authorization checks
def predict():
    if request.method == 'POST':
        # Extract data from the request
        data = request.get_json()

        # Create a DataFrame from the received data
        user_input_df = pd.DataFrame(data, index=[0])

        # Make predictions on the user input data
        predictions_prob = model.predict(user_input_df)
        predictions = (predictions_prob > 0.5).astype(int).flatten()
        predictions = predictions.tolist()  # Convert to regular Python list

        # Return the prediction result as JSON
        return jsonify({'prediction': predictions[0]})
    return jsonify({'error': 'Invalid request method'})







@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'alert')  # Use 'alert' for errors or warnings
            return redirect(url_for('register'))

        new_user = User(username=username, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful.', 'success')
        flash('An error occurred.', 'error')  # Example for an error message

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('user_dashboard' if not user.is_admin else 'admin_dashboard'))
    return render_template('login.html')


# FOR USER

@app.route('/dashboard/user')
@login_required
def user_dashboard():
    return render_template('user/user_dashboard.html')  # Updated path


# Define the CognitiveTestData model
class CognitiveTestData(db.Model):
    __tablename__ = 'cognitive_test_data'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)
    test_name = db.Column(db.String(255), nullable=False)
    test_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    drawing_data = db.Column(db.JSON, nullable=False)


# FOR USER
# Update the user_reports route to fetch user-specific cognitive test data
@app.route('/user_reports')
@login_required
def user_reports():
    cognitive_tests = CognitiveTestData.query.filter_by(username=current_user.username).all()
    return render_template('/user/user_reports.html', cognitive_tests=cognitive_tests)

@app.route('/save_cognitive_test', methods=['POST'])
@login_required
def save_cognitive_test():
    try:
        # Extract data from the request
        data = request.get_json()

        # Create a new CognitiveTestData entry
        new_test = CognitiveTestData(
            username=data['user'],
            test_name=data['test_name'],
            test_date=datetime.strptime(data['date'], "%Y-%m-%d"),
            drawing_data=json.dumps(data['drawing_data'])
        )
        db.session.add(new_test)
        db.session.commit()

        return jsonify({'message': 'Cognitive test saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})












@app.route('/dashboard/user/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Handle form submission to update the user's name and password in the database
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        # Check if the new username is already taken
        existing_user = User.query.filter(User.username == new_name).first()
        if existing_user and existing_user != current_user:
            flash('Username taken. Please choose a different username.', 'danger')
        else:
            # Update the user's name and password (if provided)
            current_user.username = new_name
            if new_password:
                current_user.set_password(new_password)
            db.session.commit()
            flash('Settings updated successfully.', 'success')

    return render_template('settings.html')


# FOR ADMIN

@app.route('/patients')
def patients():
    # Fetch data from the database (e.g., user information)
    # You'll need to implement this logic
    patients_data = User.query.all()  # Fetch all patients from the "user" table

    return render_template('admin/patients.html', patients=patients_data)

@app.route('/create_patient', methods=['POST'])
def create_patient():
    if request.method == 'POST':
        # Handle form submission to create a new patient and insert it into the database
        # Retrieve the data from the form
        name = request.form.get('name')
        # Add more fields as needed

        # Create a new user/patient in the "user" table
        new_patient = User(username=name, is_admin=False)  # Assuming "is_admin" is False for patients
        new_patient.set_password('password')  # Set a default password for the patient (you should change this)
        db.session.add(new_patient)
        db.session.commit()

        flash('Patient created successfully.', 'success')
        return redirect(url_for('patients'))  # Redirect to the patients list page
    return render_template('admin/patients.html')  # Render the patients list page



@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    # Display a form to edit the patient's information and handle form submission
    patient = User.query.get(patient_id)
    if not patient:
        flash('Patient not found.')
        return redirect(url_for('patients'))  # Redirect to the patients list page if patient not found

    if request.method == 'POST':
        # Handle form submission to update the patient's information in the database
        # Retrieve the data from the form
        name = request.form.get('name')
        # Add more fields as needed

        # Update the patient's information
        patient.username = name
        # Update other fields as needed
        db.session.commit()

        flash('Patient updated successfully.')

    return render_template('admin/patients.html', patients=User.query.all())  # Render the patients list page with updated data

@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    # Handle deletion of a patient from the database based on patient_id
    patient = User.query.get(patient_id)
    if not patient:
        flash('Patient not found.')
    else:
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully.', 'error')

    return redirect(url_for('patients'))  # Redirect back to the patients list page





@app.route('/mri_analysis')
def mri_analysis():
    # Your logic for MRI analysis goes here
    return render_template('admin/mri_analysis.html')

@app.route('/cognitive_test')
def cognitive_test():
    # Query the users from the database (replace this with your actual query)
    users = User.query.all()
    return render_template('admin/cognitive_test.html', users=users)

@app.route('/admin_reports')
@login_required  # Ensure that the user is logged in
def admin_reports():
    # Check if the user has admin privileges
    if not current_user.is_admin:
        flash('Access denied. You do not have admin privileges.', 'danger')
        return redirect(url_for('index'))  # Redirect to the homepage or another page

    # Your logic for admin reports goes here
    return render_template('admin/admin_reports.html')

@app.route('/dashboard/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('user_dashboard'))
    return render_template('admin/admin_dashboard.html')  # Updated path


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


with app.app_context():
    try:
        db.create_all()
        print("Database tables created")
    except Exception as e:
        print("Error creating database tables:", e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


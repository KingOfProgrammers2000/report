from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    mail = Mail(app)
    db = SQLAlchemy(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(60), nullable=False)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('submit'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/submit', methods=['GET', 'POST'])
    @login_required
    def submit():
        if request.method == 'POST':
            reporter_name = request.form.get('reporter_name')
            job_number = request.form.get('job_number')
            department = request.form.get('department')
            position = request.form.get('position')
            description = request.form.get('description')
            date_time = request.form.get('date_time')
            affected_person_name = request.form.get('affected_person_name')
            affected_person_age = request.form.get('affected_person_age')
            affected_person_sex = request.form.get('affected_person_sex')
            affected_person_nationality = request.form.get('affected_person_nationality')
            severity_code = request.form.get('severity_code')
            actions_taken_initiating = request.form.get('actions_taken_initiating')
            actions_taken_responding = request.form.get('actions_taken_responding')

            email_body = f"""
            Occurrence Variance Report (OVR) Submission:

            Reporter Name: {reporter_name}
            Job Number: {job_number}
            Department: {department}
            Position: {position}
            Description: {description}
            Date and Time: {date_time}
            Affected Person - Name: {affected_person_name}
            Affected Person - Age: {affected_person_age}
            Affected Person - Sex: {affected_person_sex}
            Affected Person - Nationality: {affected_person_nationality}
            Severity Code: {severity_code}
            Actions Taken by Initiating Department: {actions_taken_initiating}
            Actions Taken by Responding Department: {actions_taken_responding}
            """

            msg = Message('OVR Submission', sender=os.getenv('MAIL_USERNAME'), recipients=['aseer-kmch-aqps@moh.gov.sa'])
            msg.body = email_body

            try:
                mail.send(msg)
                flash('Report submitted and email sent successfully!', 'success')
            except Exception as e:
                flash(f'An error occurred while sending the email: {e}', 'danger')

            return redirect(url_for('index'))
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

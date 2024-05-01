from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime
import requests
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '49ac9db99be11160d14c4749083c51f74a0305dbf98d8a20bd79be7e21bf92ef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

class FeedbackForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit')
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

from flask_wtf import FlaskForm
from wtforms import StringField

class CityForm(FlaskForm):
    city = StringField('Enter City:', validators=[DataRequired()])
    submit = SubmitField('Get Weather')

THINGSPEAK_CHANNEL_ID = '2384962'
THINGSPEAK_API_KEY = 'RY6RPTQUAXQE7DXJ'
THINGSPEAK_API_URL = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        place = request.form.get('place')
        phone_number = request.form.get('phone_number')

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username is already taken. Please choose another username.', 'error')
            return render_template('signup_user.html')

        user = User(username=username, password=password, place=place, phone_number=phone_number)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setting')
def setting():
    thingspeak_data = fetch_thingspeak_data()
    return render_template('setting.html',thingspeak_data=thingspeak_data)

@app.route('/floodalert')
def floodalert():
    return render_template('flood.html')


@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback_data = Feedback(username=current_user.username, feedback=form.feedback.data)
        db.session.add(feedback_data)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))

    form.username.data = current_user.username
    feedbacks = Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)



def fetch_weather(city):
    API_KEY = "d8614ff24d40e059c1e52f8c1cc1b3d1"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, API_KEY)

    try:
        response = requests.get(current_weather_url)
        response.raise_for_status()
        weather_data = response.json()

        # Extract relevant information from the weather response
        weather_info = {
            "city": weather_data['name'],
            "temperature": round(weather_data['main']['temp'] - 273.15, 2),
            "description": weather_data['weather'][0]['description'],
            "icon": weather_data['weather'][0]['icon']
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def fetch_thingspeak_data():
    params = {'api_key': THINGSPEAK_API_KEY, 'results': 1}
    response = requests.get(THINGSPEAK_API_URL, params=params)
    data = response.json()
    
    # Extract relevant data
    if 'feeds' in data and data['feeds']:
        entry = data['feeds'][0]
        water_level = entry.get('field1', 'N/A')
        temperature = entry.get('field2', 'N/A')
        humidity = entry.get('field3', 'N/A')
        pressure = entry.get('field4', 'N/A')
        return {
            'pressure': pressure,
            'humidity': humidity,
            'water_level': water_level,
            'temperature': temperature,
        }
    return None

def generate_alerts(thingspeak_data):
    alerts = []

    if thingspeak_data is None:
        alerts.append('No data available')
        return alerts

    water_level = thingspeak_data.get('water_level')
    humidity = thingspeak_data.get('humidity')
    pressure = thingspeak_data.get('pressure')

    # Alert for flood detection
    
    if water_level and float(water_level) > 10:
        alerts.append('Flood detected!')
    else:
        alerts.append('No Flood detected!')

    if pressure is not None and humidity is not None:
        pressure = float(pressure)
        humidity = float(humidity)

        # Alert for chances of rain
        if 71.5 < humidity <= 82.5:
            alerts.append('Chances of rain detected!')
        elif pressure < 1013 and humidity < 35:
            alerts.append('Flood detected!')
        elif pressure > 1013.5 and humidity < 71.5:
            alerts.append('Less chances of rain.')

    return alerts


@app.route('/alert')
def alert():
    thingspeak_data = fetch_thingspeak_data()
    alerts = generate_alerts(thingspeak_data)
    print("Alerts:", alerts) 
    return render_template('alertpage.html', alerts=alerts)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    thingspeak_data = fetch_thingspeak_data()
  
    weather_info = None

    if request.method == 'POST':
        city = request.form.get('city')

        if city:
            weather_info = fetch_weather(city)
            if weather_info is None:
                flash("Error fetching weather data. Please enter a valid city name.Try again!")

    return render_template('dashboard.html', weather_info=weather_info, user=current_user,thingspeak_data=thingspeak_data)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('login'))
    else:
        # Handle GET request (if someone manually navigates to /logout)
        return redirect(url_for('login'))

import secrets

# Generate a secure random key with 32 bytes
secret_key = secrets.token_hex(32)

print(secret_key)


if __name__ == '__main__':
    app.run(debug=True)

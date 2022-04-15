from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Reservation, Sensor

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                           name=current_user.name,
                           sensors=Sensor.query.all(),
                           reservations=Reservation.query.filter_by(user_id=current_user.id).join(Sensor, Sensor.id == Reservation.sensor_id).add_columns(Sensor.name).all())

from flask import Blueprint, render_template, redirect, url_for, request, flash, Response, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Reservation, Sensor
from datetime import datetime, timedelta
from sqlalchemy import or_, and_

reservation = Blueprint('reservation', __name__)

datetime_format = '%Y-%m-%dT%H:%M'
datetime_format2 = '%m/%d/%Y, %H:%M:%S'

# @reservation.route('/reserve', methods=['POST'])
# @login_required
# def reserve_post():
#     user_id = current_user.id
#     sensor_id = request.form.get('sensor_id')
#     start_datetime = datetime.strptime(request.form.get('start_datetime'), datetime_format)
#     end_datetime = datetime.strptime(request.form.get('end_datetime'), datetime_format)
#     new_reservation = Reservation(user_id=user_id, sensor_id=sensor_id, start_datetime=start_datetime, end_datetime=end_datetime)
#
#     db.session.add(new_reservation)
#     db.session.commit()
#     return redirect(url_for('main.profile'))
@reservation.route('/reserve', methods=['POST'])
@login_required
def reserve_post():
    user_id = current_user.id
    start_datetime = datetime.strptime(request.form.get('start_datetime'), datetime_format2)
    end_datetime = datetime.strptime(request.form.get('end_datetime'), datetime_format2)
    selected_sensors = request.form.get('selected_sensors')[1:][:-1].split(", ")
    for sensor_id in selected_sensors:
        new_reservation = Reservation(user_id=user_id, sensor_id=sensor_id, start_datetime=start_datetime, end_datetime=end_datetime)
        db.session.add(new_reservation)
    db.session.commit()
    return redirect(url_for('main.profile'))

@reservation.route('/reserve/<id>', methods=['POST'])
@login_required
def reserve_delete(id):
    Reservation.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.profile'))


@reservation.route('/reserve/suggestions', methods=['POST'])
@login_required
def sensor_suggestions():
    cur_time = datetime.now()
    latest_time = cur_time + timedelta(hours=2)
    selected_sensors = request.form.getlist('sensor-choices')
    for i in range(0, len(selected_sensors)):
        selected_sensors[i] = int(selected_sensors[i])
    if len(selected_sensors) == 0:
        return
    reservations = Reservation.query.filter(and_(Reservation.id.in_(selected_sensors), or_(
        and_(Reservation.end_datetime >= cur_time, Reservation.end_datetime <= latest_time),
        and_(Reservation.start_datetime >= cur_time, Reservation.start_datetime <= latest_time)
    ))).order_by(Reservation.start_datetime).all()
    print(reservations)
    return render_template('profile.html',
                           name=current_user.name,
                           sensors=Sensor.query.all(),
                           selected_sensors=selected_sensors,
                           reservations=Reservation.query.filter_by(user_id=current_user.id).join(Sensor, Sensor.id == Reservation.sensor_id).add_columns(Sensor.name).all(),
                           suggestions=formatted(get_time_slots(get_free_intervals(cur_time, latest_time, reservations, []), [])))


def formatted(slots):
    for slot in slots:
        slot[0] = slot[0].strftime(datetime_format2)
        slot[1] = slot[1].strftime(datetime_format2)
    return slots


def get_free_intervals(start, end, reservations, result):
    if start >= end:
        return result
    if len(reservations) == 0:
        result.append([start, end])
        return result
    first_reservation = reservations.pop(0)
    r_start = first_reservation.start_datetime
    r_end = first_reservation.end_datetime
    if r_end < start:
        return get_free_intervals(start, end, reservations, result)
    if r_start > start:
        result.append([start, r_start])
        if r_end < end:
            return get_free_intervals(r_end, end, reservations, result)
        return result
    return get_free_intervals(r_end, end, reservations, result)


def get_time_slots(intervals, result):
    if len(intervals) == 0:
        return result
    interval = intervals.pop(0)
    slot_start = interval[0]
    slot_duration = timedelta(minutes=23)
    slot_end = slot_start + slot_duration
    while slot_end < interval[1]:
        result.append([slot_start, slot_end])
        slot_start = slot_end
        slot_end = slot_end + slot_duration
    result.append([slot_start, interval[1]])
    return get_time_slots(intervals, result)



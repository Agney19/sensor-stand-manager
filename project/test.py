from flask import Blueprint, render_template, Response, request
import cv2

from . import db
from .models import Reservation
import datetime
import os

test = Blueprint('test', __name__)


def can_operate():
    cur_time = datetime.datetime.now()
    reservation = Reservation.query.filter(Reservation.start_datetime <= cur_time, Reservation.end_datetime >= cur_time).first()
    if reservation is not None:
        return True
    else:
        return False


def gen_frames():
    # 0/1/2 - integrated webcam / usb-webcam depending on usb-connector num (left - 1, right - 2)
    camera = cv2.VideoCapture(2)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@test.route('/test')
def test_index():
    return render_template('test.html', can_operate=can_operate(), is_uploaded=False)


@test.route('/cam')
def cam():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@test.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        f.save(filename)  # hex only?
        config_file = "try_conf_unwd.cfg"
        command = "openocd -f " + config_file + " -c 'tcl_port 0' " \
                  "-c 'telnet_port 0' -c 'gdb_port 0' -c 'init' -c 'targets' " \
                  "-c 'reset halt' -c 'flash write_image erase ./" + filename + "' -c 'reset run' -c 'shutdown'"
        os.system(command)
        return render_template('test.html', can_operate=can_operate(), is_uploaded=True)

import time

from flask import Blueprint, render_template, Response, request

logs_bp = Blueprint('logs', __name__)


def generate():
    last_processed_idx = 23
    while True:
        count = None
        with open("/home/agney/Code/flask_auth_app/log.txt", "r") as file:
            count = sum(1 for _ in file)
        with open("/home/agney/Code/flask_auth_app/log.txt", "r") as file:
            last_idx = count - 1
            if last_processed_idx < last_idx:
                for i, line in enumerate(file):
                    if last_processed_idx < i < last_idx:
                        yield "{0}<br>".format(line)
                    elif i == last_idx:
                        time.sleep(0.5)
                        last_processed_idx = i
                        yield "{0}<br>".format(line)
        time.sleep(1)


@logs_bp.route('/logs')
def logs():
    return Response(generate())

from flask import Flask, make_response, render_template, request

from alchemytools.context import managed

from tioeliastanoov.constants import TioEliasStatus
from tioeliastanoov.exceptions import InvalidStatusError
from tioeliastanoov.persistence import (change_status, get_latest_status,
                                        Session)


app = Flask('tioelias', template_folder='tioeliastanoov/templates')


def get_current_status(session):
    latest_status = get_latest_status(session)
    if latest_status:
        status = latest_status.status
        latest_update = latest_status.datetime
    else:
        status = TioEliasStatus.maybe_available.value
        latest_update = None

    return status, latest_update


def get(request):
    with managed(Session) as s:
        status, latest_update = get_current_status(s)
        return make_response(render_template('index.html',
                                             status=status,
                                             latest_update=latest_update),
                             200)


def post(request):
    try:
        with managed(Session) as s:
            change_status(s, int(request.form['status']))
    except (InvalidStatusError, ValueError, KeyError):
        return '', 400
    return '', 200


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return get(request)
    else:
        return post(request)


if __name__ == '__main__':
    app.run()


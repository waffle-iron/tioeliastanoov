from flask import Flask, request

from alchemytools.context import managed

from tioeliastanoov.exceptions import InvalidStatusError
from tioeliastanoov.persistence import change_status, Session


app = Flask('tioelias')


def post(request):
    try:
        with managed(Session) as s:
            change_status(s, int(request.form['status']))
    except (InvalidStatusError, ValueError, KeyError):
        return '', 400
    return '', 200


@app.route('/', methods=['POST'])
def home():
    return post(request)


if __name__ == '__main__':
    app.run()


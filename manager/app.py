from gevent import monkey
monkey.patch_all()
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
from flask.ext.mongoengine import MongoEngine
import models
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'manger',
    'host': 'ds035240.mongolab.com',
    'port': 35240,
    'username':'ktarasz',
    'password':'ktarasz'

}

db = MongoEngine(app)

app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(5)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')


@socketio.on('recource_get', namespace='/test')
def recource_get(message):
    print message
    if hasattr(models, message['resource']):
        message.update({'status': 200,
                        'data': getattr(models, message['resource']).objects(**message['params']).to_json()})
    else:
        message.update({'status': 404, 'data': '{}'})
    print("recource_get response: {}".format(repr(message)))
    emit('recource_get', message)


@socketio.on('recource_item_get', namespace='/test')
def recource_item_get(message):
    print message
    if hasattr(models, message['resource']):
        instance = getattr(models, message['resource']).objects(**message['params']).first()
        if instance:
            message.update({'status': 200,
                            'data': instance.to_json()})
        else:
            message.update({'status': 404, 'data': 'null'})
    else:
        message.update({'status': 405, 'data': 'null'})
    print("recource_item_get response: {}".format(repr(message)))
    emit('recource_get', message)


@socketio.on('get', namespace='/test')
def get(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    page = models.Page(title='Using MongoEngine')
    page.save()
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)

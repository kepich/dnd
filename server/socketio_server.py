import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

players = []

@sio.event
def connect(sid, environ):
    players.append(sid)
    print('connect ', sid)


@sio.on('broadcast_msg')
def my_message(sid, data):
    print(f"RECEIVED[{sid}]: {data}")
    # sio.emit('update', data, skip_sid=sid)
    sio.emit('update', data)
    print(f"SENDED[{sid}]: {data}")


@sio.event
def disconnect(sid):
    players.remove(sid)
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 50022)), app)

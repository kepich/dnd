import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.on('broadcast_msg')
def my_message(sid, data):
    print(f"RECEIVED[{sid}]: {data}")
    sio.emit('update', data)
    print(f"SENDED[{sid}]: {data}")



@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 50022)), app)

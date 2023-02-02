import eventlet
import socketio

from server.Configuration import Configuration

sio = socketio.Server()
app = socketio.WSGIApp(sio)

players = {}


@sio.event
def connect(sid, environ):
    players[sid] = next(filter(lambda tpl: tpl[0] == 'nickname', environ["headers_raw"]), (sid, sid))[1]
    sio.emit('player_join', players[sid])
    # sio.emit('player_join', players[sid], skip_sid=sid)
    print('connect ', sid)


@sio.on('broadcast_msg')
def my_message(sid, data):
    sio.emit('update', data, skip_sid=sid)


@sio.event
def disconnect(sid):
    sio.emit('player_leave', players[sid], skip_sid=sid)
    del players[sid]
    print('disconnect ', sid)


if __name__ == '__main__':
    config = Configuration("server.conf")
    eventlet.wsgi.server(eventlet.listen(('', config.get_port())), app)

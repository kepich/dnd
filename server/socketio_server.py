import eventlet
import socketio

from server.Configuration import Configuration

sio = socketio.Server()
app = socketio.WSGIApp(sio)

players = {}
master = None
needs_first_load = []


@sio.event
def connect(sid, environ):

    global master
    if master is None:
        print(f"Master: {sid}")
        master = sid
        if len(players.keys()) > 0:
            needs_first_load.append(master)
            sio.emit('need_first_load', to=list(players.keys())[0])
        # else:
        #     sio.emit('first_load', data, to=master)
    else:
        print(f"Needs first load: {sid}")
        needs_first_load.append(sid)
        sio.emit('need_first_load', to=master)

    players[sid] = next(filter(lambda tpl: tpl[0] == 'nickname', environ["headers_raw"]), (sid, sid))[1]

    sio.emit('player_join', players[sid])
    print('connect ', sid)

@sio.on('first_load')
def first_load(sid, data):
    global needs_first_load

    while len(needs_first_load) > 0:
        targetSid = needs_first_load[0]
        needs_first_load.remove(targetSid)
        print(f"Send first load to: {targetSid}")
        sio.emit('first_load', data, to=targetSid)

@sio.on('broadcast_msg')
def my_message(sid, data):
    sio.emit('update', data, skip_sid=sid)


@sio.on('chat_msg')
def chat(sid, data):
    sio.emit('chat_msg', [players[sid], data])


@sio.event
def disconnect(sid):
    sio.emit('player_leave', players[sid], skip_sid=sid)
    del players[sid]

    global master
    if master == sid:
        master = None
    print('disconnect ', sid)


if __name__ == '__main__':
    config = Configuration("server.conf")
    eventlet.wsgi.server(eventlet.listen(('', config.get_port())), app)

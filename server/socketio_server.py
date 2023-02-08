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
    print(f"Connect: {sid}")
    if master is None:
        print(f"Master: {sid}")
        master = sid

        if len(players.keys()) > 0:
            print(f"need_first_load: {sid}")
            needs_first_load.append(master)
            sio.emit('need_first_load', to=list(players.keys())[0])

        print(f"master_first_load: {sid}")
        sio.emit('master_first_load', to=master)
    else:
        print(f"need_first_load: {sid}")
        needs_first_load.append(sid)
        sio.emit('need_first_load', to=master)

    players[sid] = next(filter(lambda tpl: tpl[0] == 'nickname', environ["headers_raw"]), (sid, sid))[1]

    print(f"player_join: {sid}:{players[sid]}")
    sio.emit('player_join', players[sid])


@sio.on('first_load')
def first_load(sid, data):
    global needs_first_load
    print(f"first_load: {sid}:{players[sid]}")

    while len(needs_first_load) > 0:
        targetSid = needs_first_load[0]
        needs_first_load.remove(targetSid)
        print(f"load: {sid}:{players[sid]}")
        sio.emit('load', data, to=targetSid)


@sio.on('broadcast_msg')
def my_message(sid, data):
    print(f"broadcast_msg from: {sid}")
    print(f"update from: {sid}")
    sio.emit('update', data, skip_sid=sid)


@sio.on('load')
def load(sid, data):
    print(f"load from: {sid}")
    sio.emit('load', data, skip_sid=sid)


@sio.on('chat_msg')
def chat(sid, data):
    print(f"chat_msg from: {sid}: {players[sid]}")
    sio.emit('chat_msg', [players[sid], data])


@sio.on('weather_time')
def weather(sid, data):
    print(f"weather_time from: {sid}")
    sio.emit('weather_time', data, skip_sid=sid)


@sio.on('cave_darkness')
def weather(sid, data):
    print(f"cave_darkness: {sid}:{data}")
    sio.emit('cave_darkness', data)


@sio.event
def disconnect(sid):
    print(f"disconnect: {sid}:players[sid]")
    sio.emit('player_leave', players[sid], skip_sid=sid)
    del players[sid]

    global master
    if master == sid:
        print(f"Delete master: {sid}:players[sid]")
        master = None


if __name__ == '__main__':
    config = Configuration("server.conf")
    eventlet.wsgi.server(eventlet.listen(('', config.get_port())), app)

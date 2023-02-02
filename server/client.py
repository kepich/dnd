import socketio


if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://0.0.0.0:50022')

    sio.wait()

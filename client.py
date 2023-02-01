import socket

from Configuration import Configuration


def client_program():
    config = Configuration('server.conf')

    host = config.get_server_name()
    port = config.get_port()

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = input()

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()

        print('Received from server: ' + data)
        message = input()

    client_socket.close()


if __name__ == '__main__':
    client_program()

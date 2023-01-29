import Configuration
from Configuration import Configuration
import socket


def receive_data(connections):
    data_results = []

    for connection in connections:
        data = None
        try:
            data = connection[0].recv(1024)
        except BlockingIOError:
            pass

        if not data:
            print(str(connection[1]) + ": No data")
        else:
            data = data.decode()
            print(str(connection[1]) + ": " + str(data))
            data_results.append(data)

    return data_results


def broadcast_data(connections, received_data):
    for data_sample in received_data:
        for connection in connections:
            connection[0].send(data_sample.encode())  # send data to the client


def run():
    config = Configuration('server.conf')
    max_room_size = config.get_room_size()

    server_socket = socket.socket()
    server_socket.bind((socket.gethostname(), config.get_port()))
    server_socket.listen(max_room_size)

    print("Await " + str(max_room_size) + " connections...")

    connections = []

    for _ in range(max_room_size):
        conn, address = server_socket.accept()
        conn.setblocking(False)
        print(str(address) + " connected")

        connections.append((conn, address))

    while True:
        received_data = receive_data(connections)
        broadcast_data(connections, received_data)

        if input() == "exit":
            break

    for connection in connections:
        connection[0].close()  # close the connections


if __name__ == '__main__':
    run()

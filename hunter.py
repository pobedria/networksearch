

import socket
import socketserver
import time
import threading


PORT = 9998

scales_catalogue = set()


def create_broadcast_socket():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.settimeout(2)
    return udp_sock


def ask_addresses():
    with create_broadcast_socket() as sock:
        sock.sendto('show yourself'.encode('utf-8'), ('255.255.255.255', PORT))


def update_many():
    with create_broadcast_socket() as sock:
        sock.sendto('get updates'.encode('utf-8'), ('255.255.255.255', PORT))


def update_one(ip):
    with create_broadcast_socket() as sock:
        sock.sendto('get updates'.encode('utf-8'), (ip, PORT))


class NetworkController(socketserver.StreamRequestHandler):
    def handle(self):

        request_type = self.rfile.readline()
        print("{} wrote: {}".format(self.client_address[0], request_type))
        if request_type.decode('UTF-8') == 'show\n':

            scales_catalogue.add(self.client_address[0])
            # print(scales_catalogue)

        elif request_type.decode('UTF-8') == 'get\n':
            file = open('internal.db', 'rb')
            part = file.read(1024)
            while part:
                self.wfile.write(part)
                part = file.read(1024)

            file.close()


def create_server():
    return socketserver.TCPServer(('', PORT), NetworkController)


def run_pong_server():
    server = create_server()
    server.serve_forever()


if __name__ == '__main__':
    threading.Thread(target=run_pong_server).start()

    ask_addresses()
    time.sleep(3)
    update_many()


import socket
import socketserver


PORT = 9997


class EchoServer(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.request[0].strip().decode('utf-8')
        client_ip = self.client_address[0]
        if data.startswith('show yourself'):
            print('show myself')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
                tcp_sock.connect((client_ip, PORT))
                tcp_sock.send('show\n'.encode('UTF-8'))
        elif data.startswith('get updates'):
            print('get updates FROM ')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
                tcp_sock.connect((client_ip, PORT))
                tcp_sock.send('get\n'.encode('UTF-8'))
                part = tcp_sock.recv(1024)
                file = open('internal.db', 'wb')
                while part:
                    file.write(part)
                    print(part)
                    part = tcp_sock.recv(1024)

                file.close()
        print(self.request)


def run_echo_server():
    server = socketserver.UDPServer(('', PORT), EchoServer)
    server.serve_forever()


if __name__ == '__main__':
    run_echo_server()


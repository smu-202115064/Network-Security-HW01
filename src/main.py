import socket
import ssl
import subprocess
import threading
import time


class Server:
    HOST = '0.0.0.0'
    PORT = 443
    SOCKET_BUFFER = 1024
    SERVER_KEY = 'server.key'
    SERVER_CERT = 'server.crt'

    def run(self):
        self._create_cert()
        thread = threading.Thread(target=self._host_server)
        thread.start()

    def _create_cert(self):
        print('[SERVER]: CREATE CERT')
        p = subprocess.Popen(['openssl', 'req', '-new', '-newkey', 'rsa:2048', '-days', '365', '-nodes', '-x509', '-keyout', Server.SERVER_KEY, '-out', Server.SERVER_CERT], stdin=subprocess.PIPE)
        # Country Name (2 letter code) [AU]
        p.stdin.write(bytes("KR\n", encoding='utf8'))
        p.stdin.flush()
        # State or Province Name (full name) [Some-State]
        p.stdin.write(bytes("Seoul\n", encoding='utf8'))
        p.stdin.flush()
        # Locality Name (eg, city) []
        p.stdin.write(bytes("JongRo\n", encoding='utf8'))
        p.stdin.flush()
        # Organization Name (eg, company) [Internet Widgits Pty Ltd]
        p.stdin.write(bytes("Sangmyung University\n", encoding='utf8'))
        p.stdin.flush()
        # Organizational Unit Name (eg, section) []
        p.stdin.write(bytes("AIoT\n", encoding='utf8'))
        p.stdin.flush()
        # Common Name (e.g. server FQDN or YOUR name) []
        p.stdin.write(bytes("Kim Dong Joo\n", encoding='utf8'))
        p.stdin.flush()
        # Email Address []
        p.stdin.write(bytes("hepheir@gmail.com\n", encoding='utf8'))
        p.stdin.flush()
        p.wait(timeout=10)

    def _host_server(self):
        print('[SERVER]: HOST SERVER')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((Server.HOST, Server.PORT))
        server_socket.listen(5)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=Server.SERVER_CERT, keyfile=Server.SERVER_KEY)

        # Enable TLS v1.3 support
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

        # Allow new session tickets
        # context.options |= ssl.OP_NO_TICKET

        while True:
            client_socket, addr = server_socket.accept()
            ssl_socket = context.wrap_socket(client_socket, server_side=True)

            # Handle the connection here, e.g., by reading/writing data.
            data = ssl_socket.recv(Server.SOCKET_BUFFER)
            if not data:
                continue
            ssl_socket.send(data)

        ssl_socket.close()
        server_socket.close()


class Client:
    HOST = '127.0.0.1'
    PORT = Server.PORT
    SESSION_TICKET = 'session.txt'

    def run(self):
        thread = threading.Thread(target=self._routine)
        thread.start()

    def _routine(self):
        while True:
            self.connect_full_handshake()
            self.connect_session_resumption()
            time.sleep(5)

    def connect_full_handshake(self):
        print('[CLIENT]: FULL HANDSHAKE')
        p = subprocess.Popen(['openssl', 's_client', '-connect', f'{Server.HOST}:{Server.PORT}', '-sess_out', Client.SESSION_TICKET], stdin=subprocess.PIPE)
        time.sleep(5)
        p.kill()

    def connect_session_resumption(self):
        print('[CLIENT]: SESSION RESUMPTION')
        p = subprocess.Popen(['openssl', 's_client', '-connect', f'{Server.HOST}:{Server.PORT}', '-sess_out', Client.SESSION_TICKET, '-sess_in', Client.SESSION_TICKET, '-reconnect'], stdin=subprocess.PIPE)
        time.sleep(5)
        p.kill()

if __name__ == '__main__':
    Server().run()
    Client().run()

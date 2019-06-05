import socket
import threading


class Server:
    def __init__(self, ip, port, handler):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = handler
        self.handler.s = self.s

    def start(self):
        self.s.bind((self.ip, self.port))
        print('hi')
        while (True):
            self.s.listen(5)
            conn, addr = self.s.accept()
            thread = threading.Thread(target=self.handler.handle, args=(conn,))
            thread.start()

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

    def send_msg(self, MESSAGE):
        self.s.send((MESSAGE + '\r\n').encode())

    def read_msg(self):
        data = self.s.recv(1024).decode().split('\r\n')[0]
        return data

    def close(self):
        self.s.close()


class Handler:
    def __init__(self, client):
        self.client = client

    def handle(self, s):
        data = ''
        while data != -1:
            result = 0
            # recv data - license number.
            data = s.recv(2048).decode().split('\r\n')[0]
            self.client.send_msg(data)
            result = self.client.read_msg()
            have_dis = int(result.split(',')[0])
            phone_num = result.split(',')[1]

            if have_dis == 0 and phone_num != '-':
                print('give report to: {0}'.format(phone_num))





def main():
    TCP_IP = '127.0.0.1'
    TCP_SERVER_PORT = 5402
    TCP_CLIENT_PORT = 5400

    client = Client(TCP_IP, TCP_CLIENT_PORT)
    server = Server(TCP_IP, TCP_SERVER_PORT, Handler(client))
    server.start()

if __name__ == "__main__":
    main()
import socket
import threading
import sms_sender

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
        alert_message = 'Hello {}, We noticed you parked your car, No. {} at disabled parking without having a permit. Move your car now or get a report!'
        report_message = 'Hello {}, You did not move your car, and you will get a report of 250$.'
        while data != -1:
            result = 0
            # recv data - license number.
            data = s.recv(2048).decode().split('\r\n')[0]
            report_details = data.split(',')
            alert_num = int(report_details[0])
            plate_num = report_details[1]
         
            # to the data base
            self.client.send_msg(plate_num)           
            result = self.client.read_msg()
            car_details = result.split(',')
            have_dis = int(car_details[0])
            phone_num = car_details[1]
            name = car_details[2]
            if have_dis == 0 and phone_num != '-':
                print('alert #{0}: {1}'.format(plate_num, alert_num))
                if alert_num == 1:
                    sms_sender.sendSms(phone_num, alert_message.format(name, plate_num))
                elif alert_num == 2:
                    sms_sender.sendSms(phone_num, report_message)



def main():
    TCP_IP = '127.0.0.1'
    TCP_SERVER_PORT = 5410
    TCP_CLIENT_PORT = 5401

    client = Client(TCP_IP, TCP_CLIENT_PORT)
    server = Server('0.0.0.0', TCP_SERVER_PORT, Handler(client))
    server.start()

if __name__ == "__main__":
    main()

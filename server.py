import socket
import csv
import sys
import threading


class DataBase:
  def __init__(self, filename):
    self.filename = filename
    with open(filename) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      self.dct = {row[0]:{'name':row[1], 'phone_number':row[2], 'is_disabled_car':row[3]} for row in csv_reader}
          

  def isDisabledCar(self, license_number):
    try:
      return int(self.dct[license_number]['is_disabled_car'])
    except:
      print('error')
      return 0

  def getPhoneNumber(self, license_number):
    try:
      return self.dct[license_number]['phone_number']
    except:
      return ''


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
      while(True):
        self.s.listen(5)
        conn, addr = self.s.accept()
        thread = threading.Thread(target=self.handler.handle, args=(conn,))
        thread.start()

class CarInfoHandler:
  def __init__(self, db):
    self.formatHandler = LicenceFormatValidator()
    self.dataBase = db
    
  
  def handle(self,s):
    data = ''
    while data != '-1':
        result = 0
        # recv data - license number.
        data = s.recv(2048).decode().split('\r\n')[0]
        # validate that it is a licence number format.
        if not self.formatHandler.validate(data):
            phone_number = '-'
        elif not self.dataBase.isDisabledCar(data):
            phone_number = self.dataBase.getPhoneNumber(data)
        else:
          result = 1
          phone_number = '-'
        #result_message = {
        #  "isDisabled":result,
        #  "phoneNumber":phone_number
        #}
        result_message = str(result) + "," + str(phone_number)
        print(data, phone_number)
        s.send((str(result_message)+'\r\n').encode())


class LicenceFormatValidator:
  def validate(self,licence_number):
    l = len(licence_number)
    print(l)
    return l==7 or l==8


    

  
# main:
db = DataBase('db.csv')
server = Server('127.0.0.1', 5400, CarInfoHandler(db))
server.start()

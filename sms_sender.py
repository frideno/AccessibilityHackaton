import os

def sendSms(phone_number, message):
	m = ''' curl -X POST https://api.nexmo.com/v0.1/messages \
  -u '293c88ab:DxwOVIFbbDAn6m3M'\
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
    "from": { "type": "sms", "number": "ParkingIL" },
    "to": { "type": "sms", "number": " '''+phone_number+''' " },
    "message": {
      "content": {
        "type": "text",
        "text": " '''+message+''' "
      }
    }
  }' '''
	os.system(m)



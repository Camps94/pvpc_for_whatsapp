import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import sys 
from ESIOS_Library.ESIOS import * 
from datetime import date


sys.path.insert(1, '/ESIOS_Library')
ESIOS_CREDENTIAL = os.getenv("ESIOS_CREDENTIAL")
token = ESIOS_CREDENTIAL
esios = ESIOS(token)

pvpc = esios.get_pvpc_results(token)
today = date.today()
today_format = today.strftime("%A, %d %B %Y")

message = "PVPC - {}:\n\n{}".format(today_format, pvpc)
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body=message,
                              from_='whatsapp:+34722203982',
                              to='whatsapp:+34646190000'
                          )
print(message.sid)
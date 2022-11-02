import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import sys 
from ESIOS_Library.ESIOS import * 
import datetime
import psycopg2
from babel import Locale
from babel.dates import format_date
import time

locale = Locale('es')
sys.path.insert(1, '/ESIOS_Library')
ESIOS_CREDENTIAL = os.getenv("ESIOS_CREDENTIAL")
esios = ESIOS(ESIOS_CREDENTIAL)

pvpc = esios.get_pvpc_results(ESIOS_CREDENTIAL)

today = datetime.datetime.now() + datetime.timedelta(hours=6)
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
today = format_date(today, format="full", locale='es')
resp_final = '¡Gracias por usar el servicio de alertas del PVPC!'

prices = "PVPC - Día: {}\n{} {}".format(today, pvpc, resp_final)

#open text file
text_file = open("data.txt", "w")
 
#write string to file
text_file.write(prices)
 
#close file
text_file.close()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

try:
    connection = psycopg2.connect(user = os.getenv("USER_DDBB"),
                                          password = os.getenv("PASSWORD_DDBB"),
                                          host = "ec2-52-23-131-232.compute-1.amazonaws.com",
                                          port = "5432",
                                          database = "d7l29e7ls9f6hc")
    cursor = connection.cursor()
    cursor.execute("select name from USERS WHERE status = 'TRUE'")
    numbers = cursor.fetchall()
    connection.commit()

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into users table", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

for number in numbers:
    time.sleep(2)
    message = client.messages.create(
                              body=prices,
                              from_='whatsapp:+34722203982',
                              to=number)
    print(number, ": ", message.sid, "- ", message.status)

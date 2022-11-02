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
today = today.strftime("%d%m%Y")

#today = today.replace(hour=0, minute=0, second=0, microsecond=0)
#today = format_date(today, format="full", locale='es')
#resp_final = '¡Gracias por usar el servicio de alertas del PVPC!'

#prices = "PVPC - {}: {}".format(today, pvpc)
#prices = "PVPC - {{1}}: 00:00 - {{2}} €/kWh 01:00 - {{3}} €/kWh 02:00 - {{4}} €/kWh 03:00 - {{5}} €/kWh 04:00 - {{6}} €/kWh 05:00 - {{7}} €/kWh 06:00 - {{8}} €/kWh 07:00 - {{9}} €/kWh 08:00 - {{10}} €/kWh 09:00 - {{11}} €/kWh 10:00 - {{12}} €/kWh 11:00 - {{13}} €/kWh 12:00 - {{14}} €/kWh 13:00 - {{15}} €/kWh 14:00 - {{16}} €/kWh 15:00 - {{17}} €/kWh 16:00 - {{18}} €/kWh 17:00 - {{19}} €/kWh 18:00 - {{20}} €/kWh 19:00 - {{21}} €/kWh 20:00 - {{22}} €/kWh 21:00 - {{23}} €/kWh 22:00 - {{24}} €/kWh 23:00 - {{25}} €/kWh"
#prices = "PVPC - Día: 02112022. ERROR ¡Gracias por usar el servicio de alertas del PVPC!"

prices = "PVPC - {}: 00:00 - {} €/kWh 01:00 - {} €/kWh 02:00 - {} €/kWh 03:00 - {} €/kWh 04:00 - {} €/kWh 05:00 - {} €/kWh 06:00 - {} €/kWh 07:00 - {} €/kWh 08:00 - {} €/kWh 09:00 - {} €/kWh 10:00 - {} €/kWh 11:00 - {} €/kWh 12:00 - {} €/kWh 13:00 - {} €/kWh 14:00 - {} €/kWh 15:00 - {} €/kWh 16:00 - {} €/kWh 17:00 - {} €/kWh 18:00 - {} €/kWh 19:00 - {} €/kWh 20:00 - {} €/kWh 21:00 - {} €/kWh 22:00 - {} €/kWh 23:00 - {} €/kWh".format(today, 
    pvpc[0], pvpc[1],pvpc[2],pvpc[3],pvpc[4],pvpc[5],pvpc[6],pvpc[7],pvpc[8],pvpc[9],pvpc[10],pvpc[11],pvpc[12],pvpc[13],pvpc[14],pvpc[15],pvpc[16],pvpc[17],pvpc[18],pvpc[19],pvpc[20],pvpc[21],pvpc[22],pvpc[23])

print(prices)

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


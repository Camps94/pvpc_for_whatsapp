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
today = today.strftime("%d/%m/%Y")

prices = "PVPC - {}:\n00:00 - {} EUR/kWh\n01:00 - {} EUR/kWh\n02:00 - {} EUR/kWh\n03:00 - {} EUR/kWh\n04:00 - {} EUR/kWh\n05:00 - {} EUR/kWh\n06:00 - {} EUR/kWh\n07:00 - {} EUR/kWh\n08:00 - {} EUR/kWh\n09:00 - {} EUR/kWh\n10:00 - {} EUR/kWh\n11:00 - {} EUR/kWh\n12:00 - {} EUR/kWh\n13:00 - {} EUR/kWh\n14:00 - {} EUR/kWh\n15:00 - {} EUR/kWh\n16:00 - {} EUR/kWh\n17:00 - {} EUR/kWh\n18:00 - {} EUR/kWh\n19:00 - {} EUR/kWh\n20:00 - {} EUR/kWh\n21:00 - {} EUR/kWh\n22:00 - {} EUR/kWh\n23:00 - {} EUR/kWh\n\nhttps://www.esios.ree.es/es/pvpc".format(today, 
    pvpc[0], pvpc[1],pvpc[2],pvpc[3],pvpc[4],pvpc[5],pvpc[6],pvpc[7],pvpc[8],pvpc[9],pvpc[10],pvpc[11],pvpc[12],pvpc[13],pvpc[14],pvpc[15],pvpc[16],pvpc[17],pvpc[18],pvpc[19],pvpc[20],pvpc[21],pvpc[22],pvpc[23])

print(prices)

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
    cursor.execute("select name from USERS WHERE status = 'FALSE'")
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
    #time.sleep(1)
    message = client.messages.create(
                              body=prices,
                              from_='whatsapp:+34722203982',
                              to='whatsapp:+34646190000')
    print(number, ": ", message.sid, "- ", message.status)


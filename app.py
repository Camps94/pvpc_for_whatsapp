from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import date
import sys
import os
import psycopg2
from ESIOS_Library.ESIOS import * 

try:
    from collections.abc import Container, Iterable, MutableSet
except ImportError:
    from collections import Container, Iterable, MutableSet

sys.path.insert(1, '/ESIOS_Library')
ESIOS_CREDENTIAL = os.getenv("ESIOS_CREDENTIAL")



token = ESIOS_CREDENTIAL
esios = ESIOS(token)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms2", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()
    #var = get_pvpc_results()
    var = esios.get_pvpc_results(token)
    today = date.today()
    d2 = today.strftime("%A, %d %B %Y")

    if msg == "PVPC" or msg == "pvpc":
        resp.message("PVPC - {}:\n\n{}".format(d2, var))
    else:
        resp.message("Hi, You said: {}. If you want to get the PVPC prices for today, reply PVPC. ".format(msg))

    return str(resp)

@app.route("/sms", methods=['POST'])
def updateDDBB():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    user = request.form.get('To')
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()

    if msg == "activate" or msg == "on":
        resp.message("PVPC Reminder has been activated")
        action = 'TRUE'
    elif msg == "deactivate" or msg == "off":
        action = 'FALSE'
        resp.message("PVPC Reminder has been deactivated")

    try:
        connection = psycopg2.connect(user = "swhbwiqxmvmmmn",
                                          password = "91d7c8ccca212adc1bed8d3a3836da935a9490aa03596f70edc80850f75c2453",
                                          host = "ec2-52-23-131-232.compute-1.amazonaws.com",
                                          port = "5432",
                                          database = "d7l29e7ls9f6hc")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name , status) VALUES (%s, %s)", (user, action))
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

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

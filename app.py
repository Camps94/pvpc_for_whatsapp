from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import date
import sys
import os
import psycopg2
from ESIOS_Library.ESIOS import * 

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/ddbb", methods=['POST'])
def updateDDBB():

    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    number = request.form.get('From')
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()

    if msg == "activate" or msg == "on" or msg == "ON":
        resp.message("PVPC Reminder has been activated")
        action = 'TRUE'
    elif msg == "deactivate" or msg == "off" or msg == "OFF":
        action = 'FALSE'
        resp.message("PVPC Reminder has been deactivated")
    else: 
        resp.message("Please, reply ON or OFF to activate or deactivate the PVPC Reminder")

    try:
        connection = psycopg2.connect(user = os.getenv("USER_DDBB"),
                                          password = os.getenv("PASSWORD_DDBB"),
                                          host = "ec2-52-23-131-232.compute-1.amazonaws.com",
                                          port = "5432",
                                          database = "d7l29e7ls9f6hc")
        cursor = connection.cursor()
        #cursor.execute("INSERT INTO users (name , status) VALUES (%s, %s)", (number, action))
        sql_query = "UPDATE users SET status = {} WHERE name = {}".format(action, number)
        cursor.execute(sql_query)
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

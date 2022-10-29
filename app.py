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
    msg = msg.lower()

    try:
        connection = psycopg2.connect(user = os.getenv("USER_DDBB"),
                                          password = os.getenv("PASSWORD_DDBB"),
                                          host = "ec2-52-23-131-232.compute-1.amazonaws.com",
                                          port = "5432",
                                          database = "d7l29e7ls9f6hc")
        cursor = connection.cursor()    
        # Create reply
        resp = MessagingResponse()
        if msg == "alta":
            action = 'TRUE'        
            resp.message("PVPC Reminder has been activated")
            sql_query = "INSERT INTO users (name, status) VALUES ('{}', '{}') ON CONFLICT (name) DO UPDATE SET status = '{}';".format(number, action, action)        
            cursor.execute(sql_query)
            connection.commit()

        elif msg == "baja":
            action = 'FALSE'
            resp.message("PVPC Reminder has been deactivated")
            sql_query = "INSERT INTO users (name, status) VALUES ('{}', '{}') ON CONFLICT (name) DO UPDATE SET status = '{}';".format(number, action, action)        
            cursor.execute(sql_query)
            connection.commit()

        else:
            resp.message("Por favor, envíe la palabra *ALTA* o *BAJA* para darse de ALTA/BAJA en el servicio de alarma del PVPC")

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

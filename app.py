from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import date
import sys
import os
from collections.abc import Container, Iterable, MutableSet


sys.path.insert(1, '/ESIOS_Library')
ESIOS_CREDENTIAL = os.getenv("ESIOS_CREDENTIAL")

from ESIOS_Library.ESIOS import * 

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
    elif msg == "deactivate" or msg == "off":
        resp.message("PVPC Reminder has been deactivated")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

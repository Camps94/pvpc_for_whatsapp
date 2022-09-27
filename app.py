from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
#from get_pvpc import get_pvpc_results

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()
    if msg == "PVPC":
        resp.message("Hi, You said: {}. If you want to get the PVPC for tommorow, reply PVPC. ".format("OKEEEEY"))
    else:
        resp.message("Hi, You said: {}. If you want to get the PVPC for tommorow, reply PVPC. ".format(msg))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

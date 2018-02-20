#!/usr/bin/env python

import urllib
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os

 
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    action= req.get("result").get("action")
    
    result = req.get("result")
    parameters = result.get("parameters")
    statev = parameters.get("state")
    if(action=="bulb"):
        if(statev=="on"):
            y="https://api.thingspeak.com/update?api_key=4NJNCSZCV75GDEG9&field1=1"
        elif(statev=="off"):
            y="https://api.thingspeak.com/update?api_key=4NJNCSZCV75GDEG9&field1=0"
    elif(action=="fan"):
        if(statev=="on"):
            y="https://api.thingspeak.com/update?api_key=4NJNCSZCV75GDEG9&field1=1"
        elif(statev=="off"):
            y="https://api.thingspeak.com/update?api_key=4NJNCSZCV75GDEG9&field1=0"
    elif(action=="ac"):
        if(statev=="on"):
            y="https://api.thingspeak.com/update?api_key=4NJNCSZCV75GDEG9&field1=1"
        elif(statev=="off"):
            y="https://api.thingspeak.com/update?api_key=4NJNCSZCV75GDEG9&field1=0"
    result=urlopen(y).read()
    speech =str(result)
    if(speech=="b'0'"):
        speech="I missed that whatever you say,Try again"
    elif(speech!="b'0'"):
        speech="OKay! I have done it."
        

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "SauR automation webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')

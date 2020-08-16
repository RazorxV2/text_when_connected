import sys
import subprocess 
import os
import json
import webbrowser
from twilio.rest import Client

#Loads Config file
with open('config.json') as f:
    config = json.load(f)

IP_DEVICE = config["IP_DEVICE"]
ACCOUNT_SID = config["ACCOUNT_SID"]
AUTH_TOKEN = config["AUTH_TOKEN"]
TWILIO_NUM = config["TWILIO_NUM"]
USER_NUM = config["USER_NUM"]

#Runs a ping command for a specified IP address, and when a reply is received returns true
def check_for_phone():
    proc = subprocess.Popen(["ping", IP_DEVICE, "-t"],stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        #Splits the response into an array, and if there is a response, the device IP will be in the 3rd position of the aray
        #Checks that the returned IP matches the device IP
        connected_ip = line.decode('utf-8').split()
        if len(connected_ip) > 2: #Helps filter out bad responses
            #IP returns with colon appended. Need to compare without the colon 
            if connected_ip[2][:-1] == IP_DEVICE:
                return True

#code to send text
def send_text():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        to= USER_NUM,
        from_= TWILIO_NUM,
        body='You are connected!')
    print(message.sid)

def main():    
    while True:
        if check_for_phone():
            send_text()
            break

if __name__ == "__main__":
    main()
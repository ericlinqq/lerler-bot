import requests
import os

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {"message": msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    
    return r.status_code

message = "Notify from LINE, Hello world!"
token = os.getenv("NOTIFY_TOKEN")

if __name__ == "__main__":
    lineNotifyMessage(token, message)
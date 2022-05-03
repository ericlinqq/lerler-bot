import requests
import configparser

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {"message": msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    
    return r.status_code

message = "Notify from LINE, Hello world!"
config = configparser.ConfigParser()
config.read('./config.ini')
token = config.get('notify', 'NOTIFY_TOKEN')

if __name__ == "__main__":
    lineNotifyMessage(token, message)
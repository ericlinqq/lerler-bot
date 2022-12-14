import requests
import time
import redis
import os

url = 'https://api.binance.com'
symbol = 'ETHUSDT'

# IFTTT
token = os.getenv("IFTTT_TOKEN")

# Redis lab
redisHost = os.getenv("HOST")
redisPort = os.getenv("PORT")
redisPwd = os.getenv("PASSWORD")

useRedis = redis.Redis(
    host = redisHost,
    port = redisPort,
    password = redisPwd
)

def getPrice(url, symbol):
    try:
        data = requests.get(url + '/api/v3/ticker/price', params={'symbol': symbol}).json()
        return data
    except Exception as e:
        print("Error! problem is {}".format(e.args[0]))

def lineNotifyMessage(token, symbol, msg):
    r = requests.get('https://maker.ifttt.com/trigger/crypto_alert/with/key/'+token+'?value1='+str(symbol)+'&value2='+str(msg))
    if r.text[:5] == "Congr":
        print("【{}】成功推送 ({}) 至 Line".format(str(symbol), str(msg)))
    return r.text

if __name__ == "__main__":
    prev_price = -1
    while True: 
        setPrice_above = float(useRedis.get("above"))
        print("上穿價: %f" %(setPrice_above))
        setPrice_below = float(useRedis.get("below"))
        print("下穿價: %f" %(setPrice_below))
        data = getPrice(url, symbol)
        current_price = float(data['price'])
        print("目前價: %f" %(current_price))
        if prev_price != -1:
            if  prev_price < setPrice_above and current_price > setPrice_above:
                msg = '【上穿】<br>目前價格: %f<br>目前設定上穿價格: %f' %(current_price, setPrice_above) 
                print("上穿")
                lineNotifyMessage(token, symbol, msg)

            if prev_price > setPrice_below and current_price < setPrice_below:
                msg = '【下穿】<br>目前價格: %f<br>目前設定下穿價格: %f' %(current_price, setPrice_below)
                print("下穿")
                lineNotifyMessage(token, symbol, msg) 
        print("----------------")
        prev_price = current_price
        time.sleep(30)

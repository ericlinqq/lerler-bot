import requests
import configparser
import time
import redis

url = 'https://api.binance.com'
symbol = 'ETHUSDT'
config = configparser.ConfigParser()
config.read('config.ini')

# IFTTT
token = config.get('ifttt', 'IFTTT_TOKEN')

# Redis lab
redisHost = config.get('redis-lab', 'HOST')
redisPort = config.get('redis-lab', 'PORT')
redisPwd = config.get('redis-lab', 'PASSWORD')

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

def lineNotifyMessage(token, msg):
    r = requests.get('https://maker.ifttt.com/trigger/crypto_alert/with/key/'+token+'?value1='+str(msg))
    if r.text[:5] == "Congr":
        print("成功推送 ({}) 至 Line".format(str(msg)))
    return r.text

if __name__ == "__main__":
    prev_price = -1
    while True: 
        setPrice_above = float(useRedis.get("above"))
        print("上穿價: %.2f" %(setPrice_above))
        setPrice_below = float(useRedis.get("below"))
        print("下穿價: %.2f" %(setPrice_below))
        data = getPrice(url, symbol)
        current_price = float(data['price'])
        print("目前價: %.2f" %(current_price))
        if prev_price != -1:
            if  prev_price < setPrice_above and current_price > setPrice_above:
                msg = '【上穿】<br>目前價格: %.2f<br>目前設定上穿價格: %f' %(current_price, setPrice_above) 
                print("上穿")
                lineNotifyMessage(token, msg)

            if prev_price > setPrice_below and current_price < setPrice_below:
                msg = '【下穿】<br>目前價格: %.2f<br>目前設定下穿價格: %f' %(current_price, setPrice_below)
                print("下穿")
                lineNotifyMessage(token, msg) 
        print("----------------")
        prev_price = current_price
        time.sleep(30)

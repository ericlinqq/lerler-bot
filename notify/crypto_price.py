import requests
import configparser
import time

url = 'https://api.binance.com'
symbol = 'ETHUSDT'

def getPrice(url, symbol):
    try:
        data = requests.get(url + '/api/v3/ticker/price', params={'symbol': symbol}).json()
    except Exception as e:
        print("Error! problem is {}".format(e.args[0]))
    
    return data

def lineNotifyMessage(token, msg):
    r = requests.get('https://maker.ifttt.com/trigger/crypto_alert/with/key/'+token+'?value1='+str(msg))
    if r.text[:5] == "Congr":
        print("成功推送 ({}) 至 Line".format(str(msg)))
    return r.text

if __name__ == "__main__":
    prev_price = -1
    while True:
        config = configparser.ConfigParser()
        config.read('./config.ini')
        token = config.get('ifttt', 'IFTTT_TOKEN')
        setPrice_above = float(config.get('ifttt', 'SETPRICE_ABOVE'))
        setPrice_below = float(config.get('ifttt', 'SETPRICE_BELOW'))
        data = getPrice(url, symbol)
        current_price = float(data['price'])
        
        if prev_price != -1:
            if  prev_price < setPrice_above and current_price > setPrice_above:
                msg = '【上穿】目前價格: {}<br>目前設定上穿價格: {}'.format(data['price'], str(setPrice_above)) 
                lineNotifyMessage(token, msg)

            if prev_price > setPrice_below and current_price < setPrice_below:
                msg = '【下穿】目前價格: {}<br>目前設定下穿價格: {}'.format(data['price'], str(setPrice_below))
                lineNotifyMessage(token, msg) 
        
        prev_price = current_price
        time.sleep(10)

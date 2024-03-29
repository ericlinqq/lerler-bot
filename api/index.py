from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, JoinEvent, PostbackEvent, TextMessage, StickerMessage, TextSendMessage, StickerSendMessage, FlexSendMessage, ImageSendMessage
from GPT.chatGPT import ChatGPT
from food.foodScraper import IFoodie
from food.message import AreaMessage, CategoryMessage, PriceMessage
from weather.weather import CWB
from notify.crypto_price import getPrice


import os
import redis

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING") if os.getenv("DEFALUT_TALKING") else True

# Redis lab
redisHost = "redis-17017.c241.us-east-1-4.ec2.cloud.redislabs.com"
redisPort = "17017"
redisPwd = os.getenv("PASSWORD")

useRedis = redis.Redis(
    host = redisHost,
    port = redisPort,
    password = redisPwd
)
# 設定價格並儲存至Redis Lab
def setPrice(type, event):
    try:
        price = float(event.message.text[7:])
        useRedis.set(type, price)
        message = TextSendMessage(text='價格設定成功! \n%s' %(event.message.text[2:]))
    except Exception as e:
        print("Error! problem is {}".format(e.args[0]))
        message = TextSendMessage(text='設定格式為: 設定(上穿or下穿)價格 【價格】')
    return message

app = Flask(__name__)
chatgpt = ChatGPT()

# Weather valid cities
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣'\
                    ,'新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']

# domain root 
@app.route('/')
def home():
    return 'Hello, World!'
    
@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 加入好友訊息
@line_handler.add(FollowEvent)
def handle_follow(event):
    message = TextSendMessage(text="喵~我是樂樂")
    line_bot_api.reply_message(event.reply_token, message)
# 加入群組訊息
@line_handler.add(JoinEvent)
def handle_join(event):
    message = TextSendMessage(text="喵~我是樂樂")
    line_bot_api.reply_message(event.reply_token, message)

# 處理貼圖訊息
@line_handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    message = StickerSendMessage(
        package_id = '11537',
        sticker_id = '52002753'
    )
    line_bot_api.reply_message(event.reply_token, message)

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    if event.message.type != "text":
        return

    if event.message.text == "說話":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ "))
        return

    if event.message.text == "閉嘴":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <"))
        return

    if working_status:
        chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))
    
    message = ''

    # 美食「選擇地區」樣板類別訊息
    if event.message.text == "美食":
        message = FlexSendMessage(
            '[美食] 請選擇地區',
            AreaMessage().content()
        )
    
    # 天氣樣板類別訊息
    elif event.message.text[:2] == "天氣":
        city = event.message.text[3:]
        city = city.replace('台', '臺')
        # 使用者輸入的內容並非符合格式
        if not (city in cities):
            message = TextSendMessage(text='查詢格式為: 天氣 【縣市】')
        else:
            weather = CWB(city)
            
            message = FlexSendMessage(
                '[天氣] '+city+'未來36小時天氣預測', 
                weather.get()
                )
    
    # 樂樂照片
    elif event.message.text.find("樂樂") != -1 :
        message = ImageSendMessage(
            original_content_url = 'https://i.imgur.com/SuatGGC.jpg',
            preview_image_url = 'https://i.imgur.com/SuatGGC.jpg')
    
    # 查詢幣安價格
    elif event.message.text[:4] == "目前價格":
        coin = event.message.text[5:]
        res = getPrice('https://api.binance.com', coin)
        message = TextSendMessage(text='【%s】\n目前價格為: %f' %(coin, float(res['price'])))

    # Line Notify設定價格提醒 
    elif event.message.text[:2] == "設定":
        if event.message.text[2:6] == "上穿價格": 
            message = setPrice("above", event)

        elif event.message.text[2:6] == "下穿價格":
            message = setPrice("below", event)
    
    # Line Notify設定價格查詢
    elif event.message.text == "查詢設定價格":
        above = float(useRedis.get("above"))
        below = float(useRedis.get("below"))
        message = TextSendMessage(text='目前設定價格:\n上穿價格: %f\n下穿價格: %f' %(above, below))

    if message != '':
        line_bot_api.reply_message(event.reply_token, message)

# 處理美食回傳值事件
@line_handler.add(PostbackEvent)
def handle_postback(event):
    message = ''
    if event.postback.data[0] == "A":  # 如果回傳值為「選擇地區」
        message = FlexSendMessage(
            '[美食] 請選擇美食類別',
            CategoryMessage(event.postback.data[2:]).content()
        )

    elif event.postback.data[0] == "B":  # 如果回傳值為「選擇美食類別」
        message = FlexSendMessage(
            '[美食] 請選擇消費價格',
            PriceMessage(event.postback.data[2:]).content()
        )
    elif event.postback.data[0] == "C":  # 如果回傳值為「選擇消費金額」
        result = event.postback.data[2:].split('&')

        food = IFoodie(
            result[0], # 地區 
            result[1], # 美食類別
            result[2]  # 消費金額
        )
        restaurants = food.scrape()
        if restaurants == '':
            message = TextSendMessage(text="找不到搜尋結果喵~")
        
        else:
            message = FlexSendMessage(
                '[美食] 目前營業中的前十大人氣餐廳',
                restaurants
            )

    elif event.postback.data[0] == "D":
        message = TextSendMessage(text="我也要吃喵~")
    if message != '':    
        line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    app.run()
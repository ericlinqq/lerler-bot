from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,
    MessageEvent,
    PostbackEvent,
    TextSendMessage,
    TextMessage,
    StickerSendMessage,
    StickerMessage,
    ImageSendMessage
)

import configparser

from foodScraper import IFoodie

from message import AreaMessage, CategoryMessage, PriceMessage

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

# Channel Access Token
line_bot_api = LineBotApi(config.get('line-bot', 'CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(config.get('line-bot', 'CHANNEL_SECRET'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 加入好友歡迎訊息
@handler.add(FollowEvent)
def handle_follow(event):
    message = TextSendMessage(text="喵~我是樂樂")
    line_bot_api.reply_message(event.reply_token, message)

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = ''
    # 美食「選擇地區」樣板類別訊息
    if event.message.text == "美食":
        message = AreaMessage().content()  
    # 樂樂照片
    elif event.message.text == "樂樂":
        message = ImageSendMessage(
            original_content_url = 'https://i.imgur.com/SuatGGC.jpg',
            preview_image_url = 'https://i.imgur.com/SuatGGC.jpg'
        )
    if message != '':
        line_bot_api.reply_message(event.reply_token, message)

# 處理美食回傳值事件
@handler.add(PostbackEvent)
def handle_postback(event):
    message = ''
    print(event.postback.data)
    if event.postback.data[:1] == "A":  # 如果回傳值為「選擇地區」
        message = CategoryMessage(event.postback.data[2:]).content()
    elif event.postback.data[:1] == "B":  # 如果回傳值為「選擇美食類別」
        message = PriceMessage(event.postback.data[2:]).content()
    elif event.postback.data[:1] == "C":  # 如果回傳值為「選擇消費金額」
        result = event.postback.data[2:].split('&')

        food = IFoodie(
            result[0], # 地區 
            result[1], # 美食類別
            result[2]  # 消費金額
        )

        message = TextSendMessage(text=food.scrape())

    if message != '':
        line_bot_api.reply_message(event.reply_token, message)

# 處理貼圖訊息
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    message = StickerSendMessage(
        package_id = '11537',
        sticker_id = '52002753'
    )
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
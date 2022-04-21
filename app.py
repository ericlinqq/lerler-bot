from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import configparser

from foodScraper import IFoodie

app = Flask(__name__)

config = configparser.Configparser()
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

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 美食爬蟲
    if "美食" in event.message.text:
        food = IFoodie(event.message.text[2:])
        message = TextSendMessage(text=food.scrape())

    if "樂樂" in event.message.text:
        message = ImageSendMessage(
            original_content_url = 'https://i.imgur.com/SuatGGC.jpg',
            preview_image_url = 'https://i.imgur.com/SuatGGC.jpg'
        )
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
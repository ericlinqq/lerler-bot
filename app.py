from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('IqHOXvZP7ZJdexo6qige4/p9JCZGopk92X5fw0NqiU/TZ74ql7EsM8YwlBTdY8jopd/gPIV4QeBP85WCbxRIhfd/ivcHwbwrV9InPjhCehWYYnOItvuEaAQwSLpt2JkdyJPjWLUCi+ezHgITvps6VQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('46c7b04da56c9338821f32f53c5e85c9')

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = "喵~"if len(event.message.text) > 5 else "..."
    message = TextSendMessage(text=text)
    line_bot_api.reply_message(event.reply_token, message)
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    message = StickerSendMessage(
        package_id = '1',
        sticker_id = '1'
    )
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
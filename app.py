import os
from datetime import datetime

from flask import Flask, abort, request

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('qC/dQX0XuVYkhZyVA5kUj8YMs4f+dFZ09MZ3zG0+fB5K7JzrcTDqIYB/GaANn9SjaUJJzCMTXstom3Gs+cAepid4jjNY2k1woRfsI6zbXCaG4oJFbezc9RUMHrN+lM67HRmCYqkEKmZdiyrCPC8dfAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('abba63a31e52b3e057531d672e88d31d')
print('app = Flask(__name__)')

@app.route("/", methods=["GET", "POST"])
def callback():
    if request.method == "GET":
        return "Hello Heroku"

    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']
        # get request body as text
        body = request.get_data(as_text=True)
 
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    app.run(debug=True, port=80)
    
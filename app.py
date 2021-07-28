from flask import Flask, request, abort

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    
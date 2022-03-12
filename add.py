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

line_bot_api = LineBotApi('/IQk36hMk8CKDBKdVqf5FySy3IVl9np6ZL/W5ZuV6u6GckPSfNDtjUWkcjVME3F0cZU5q/t5JoHn+WoTdyuUWUVZpqfWY2Nrwz1n0c40WlCGPPRiZMpfsQLKYQ3oMyMSg8unQu8ax5CmfpVHmO2nvwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('13b84f1a1c67134e14e77295d7846e2f')


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
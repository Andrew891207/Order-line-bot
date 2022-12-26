import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["lobby", "user", "menu", "rec_coffee", "cal_dessert", "intro", "bitter",
     "bitter_first", "bitter_second", "bitter_third", "sour", "sour_first", "sour_second", "sour_third", 
     "brownie", "scone", "muffin", "cookie", "order", "cash", "order1", "order2"],
    transitions=[
        {"trigger": "advance", 'source': 'user', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'lobby', 'dest': 'menu', 'conditions': 'is_going_to_menu'},
        {"trigger": "advance", 'source': 'lobby', 'dest': 'rec_coffee', 'conditions': 'is_going_to_rec_coffee'},
        {"trigger": "advance", 'source': 'lobby', 'dest': 'cal_dessert', 'conditions': 'is_going_to_cal_dessert'},
        {"trigger": "advance", 'source': 'lobby', 'dest': 'intro', 'conditions': 'is_going_to_intro'},
        {"trigger": "advance", 'source': 'intro', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'rec_coffee', 'dest': 'bitter', 'conditions': 'is_going_to_bitter'},
        {"trigger": "advance", 'source': 'bitter', 'dest': 'bitter_first', 'conditions': 'is_going_to_bitter_first'},
        {"trigger": "advance", 'source': 'bitter', 'dest': 'bitter_second', 'conditions': 'is_going_to_bitter_second'},
        {"trigger": "advance", 'source': 'bitter', 'dest': 'bitter_third', 'conditions': 'is_going_to_bitter_third'},
        {"trigger": "advance", 'source': 'bitter_first', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'bitter_second', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'bitter_third', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'rec_coffee', 'dest': 'sour', 'conditions': 'is_going_to_sour'},
        {"trigger": "advance", 'source': 'sour', 'dest': 'sour_first', 'conditions': 'is_going_to_sour_first'},
        {"trigger": "advance", 'source': 'sour', 'dest': 'sour_second', 'conditions': 'is_going_to_sour_second'},
        {"trigger": "advance", 'source': 'sour', 'dest': 'sour_third', 'conditions': 'is_going_to_sour_third'},
        {"trigger": "advance", 'source': 'sour_first', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'sour_second', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'sour_third', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'cal_dessert', 'dest': 'brownie', 'conditions': 'is_going_to_brownie'},
        {"trigger": "advance", 'source': 'cal_dessert', 'dest': 'muffin', 'conditions': 'is_going_to_muffin'},
        {"trigger": "advance", 'source': 'cal_dessert', 'dest': 'scone', 'conditions': 'is_going_to_scone'},
        {"trigger": "advance", 'source': 'cal_dessert', 'dest': 'cookie', 'conditions': 'is_going_to_cookie'},
        {"trigger": "advance", 'source': 'brownie', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'muffin', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'scone', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'cookie', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'menu', 'dest': 'order', 'conditions': 'is_going_to_order'},
        {"trigger": "advance", 'source': 'order', 'dest': 'order1', 'conditions': 'is_going_to_order1'},
        {"trigger": "advance", 'source': 'order1', 'dest': 'order2', 'conditions': 'is_going_to_order2'},
        {"trigger": "advance", 'source': 'order2', 'dest': 'order1', 'conditions': 'is_going_to_order1'},
        {"trigger": "advance", 'source': 'order2', 'dest': 'cash', 'conditions': 'is_going_to_cash'},
        {"trigger": "advance", 'source': 'order1', 'dest': 'cash', 'conditions': 'is_going_to_cash'},
        {"trigger": "advance", 'source': 'cash', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        {"trigger": "advance", 'source': 'menu', 'dest': 'lobby', 'conditions': 'is_going_to_lobby'},
        
        
        #{"trigger": "go_back", "source": [], "dest": "user"},
        
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if (event.message.text=='fsm'):
                show_fsm()
            elif (machine.state=='user'):
                send_text_message(event.reply_token, "請輸入【選單】")
            else:
                send_text_message(event.reply_token, "把字打對很難嗎?")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.jpg", prog="dot", format="jpg")
    return send_file("fsm.jpg", mimetype="image/jpg")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)#123
    app.run(host="0.0.0.0", port=port, debug=True)

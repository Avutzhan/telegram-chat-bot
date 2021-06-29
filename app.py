from flask import Flask, request
from mediodok_bot.credentials import TOKEN
import requests
import json

app = Flask(__name__)


def send_message(chat_id, text=None, parse_mode=None, key=None):
    if key is None:
        key = {}
    method = "sendMessage"
    token = TOKEN
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "reply_markup": key}
    requests.post(url, data=data)


def start(chat_id):
    send_message(chat_id, "Вас приветствует <b>Бот Помошник Информатор Нотификатор</b> компании Медиодок.\n"
                          "Введите команду /help чтобы получить дополнительную информацию о командах!", "HTML")


def help(chat_id):
    send_message(chat_id, "Все команды.\n"
                          "/help - дополнительная информация о командах!\n"
                          "/start - начало работы приветствие\n"
                          "/number - отправить свой номер", "HTML")


def handle_number(chat_id):
    keyboard = {"keyboard": [
        [{
            "text": "My phone number",
            "request_contact": True
        }]
    ], "one_time_keyboard": True}
    key = json.JSONEncoder().encode(keyboard)
    send_message(chat_id, "write the number", "HTML", key)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
        chat_id = request.json["message"]["chat"]["id"]

        # handle /start command
        start_command = request.json["message"].get("text")
        if start_command and start_command == "/start":
            start(chat_id)

        # handle /help command
        help_command = request.json["message"].get("text")
        if help_command and help_command == "/help":
            help(chat_id)

        # handle /number command
        number_command = request.json["message"].get("text")
        if number_command and number_command == "/number":
            handle_number(chat_id)

        # handle action after number enter
        number = request.json["message"].get("contact")
        chat_id = request.json["message"]["chat"]["id"]
        if number:
            print("thereis number")
            send_message(chat_id, request.json["message"]["contact"]["phone_number"])
        else:
            print("no number")

    return {"ok": True}

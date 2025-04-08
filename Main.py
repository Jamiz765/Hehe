import openai
import os
from flask import Flask, request
import telegram

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GPT_KEY = os.getenv("OPENAI_API_KEY")
bot = telegram.Bot(token=TOKEN)
openai.api_key = GPT_KEY

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message.text

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a smart chill bot."},
            {"role": "user", "content": message}
        ]
    )
    reply = gpt_response['choices'][0]['message']['content']
    bot.send_message(chat_id=update.message.chat_id, text=reply)
    return "ok"

@app.route("/")
def home():
    return "Bot is alive"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))

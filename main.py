from flask import Flask, request, Response
import telegram
import os
import botfunc


TOKEN = os.environ.get("TOKEN")
URL = os.environ.get("URL")

app = Flask(__name__)

TOKEN = '5535320183:AAF_wqhZNEQ5yIqAGwtesGBxtIHrlrLJG9I'
bot = telegram.Bot(token=TOKEN)
URL = "https://c90f-139-47-18-90.eu.ngrok.io"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        chat_id, txt, username = botfunc.tel_parse_message(update)
        if txt.lower() == '/start':
            # This launchs the welcome message
            botfunc.start(chat_id=chat_id, username=username, bot=bot)

        elif txt.lower() == 'help':
            # The help message will send a message to the user, showing all commands
            botfunc.user_help(chat_id=chat_id, bot=bot)

        elif txt.split(" ")[0].lower() == 'roll':
            # It rolls a dice
            botfunc.roll(bot=bot, chat_id=chat_id, username=username, txt=txt)

        elif txt.split(" ")[0].lower() == 'stock':
            # Show the stock changes of a company the user chose.
            try:
                txt.split(" ")[1]

            except IndexError:
                botfunc.incomplete_stock(bot=bot, chat_id=chat_id)

            else:
                messages = botfunc.stock(txt.split(" ")[1],  os.environ.get("ALP_KEY"), os.environ.get("NEWS_API_KEY"))
                for message in messages:
                    bot.send_message(chat_id=chat_id, text=message)
        elif txt.lower() == "anime":
            # Show a anime picture
            botfunc.anime_img(bot=bot, chat_id=chat_id)
        return Response('ok', status=200)
    else:
        return "<h1>Welcome</h1>"


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook(URL)
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

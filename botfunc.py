import random
import data
from stockview import StockView


def tel_parse_message(message):
    """This will allow us to scrape all the data that the json is giving us, and use the parts that we need. It
    returns chat_id and txt."""
    chat_id = message.message.chat_id
    txt = message.message.text
    user_name = message.message.chat.first_name

    return chat_id, txt, user_name


def start(bot, chat_id, username):
    bot.send_message(chat_id=chat_id, text=f"Welcome to {username} Santiago Bot,"
                                           f" I'm here to make all your dreams come true! "
                                           f"Type 'help' if you want to see all the available commands")


def user_help(bot, chat_id):
    bot.send_message(chat_id=chat_id, text="Commands available:\n🤖 roll\n🤖 stock\n🤖 anime")


def roll(bot, chat_id, username, txt):
    try:
        roll_number = int(txt.split(" ")[1])
    except IndexError:
        bot.send_message(chat_id=chat_id, text="Please select a number for the dice (e.g: 'roll 20')")
    else:
        random_number = random.randint(1, roll_number)
        bot.send_message(chat_id=chat_id, text=f"🎲 {username}, you got a {random_number} 🎲")


def anime_img(bot, chat_id):
    choice = random.choice(data.anime)
    bot.send_photo(chat_id=chat_id, photo=choice)


def incomplete_stock(bot, chat_id):
    bot.send_message(chat_id=chat_id, text="You have to select a company:")
    for company in data.companies:
        bot.send_message(chat_id=chat_id,
                         text=f"{company} {data.companies[company]['symbol']} - {data.companies[company]['name']}")
    bot.send_message(chat_id=chat_id, text=f"e.g: 'stock 6'")


def stock(num, alp_key, news_api_key):
    my_stock = StockView(num, alp_key, news_api_key)
    messages = my_stock.get_percentage()
    return messages
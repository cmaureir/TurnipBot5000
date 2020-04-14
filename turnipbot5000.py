import re
import logging
import configparser

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

from lib.spreadsheet import get_last, get_prev
from lib.critters import (format_similar_names, get_similar_names,
                          format_info, get_info)



def test(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="It's working")


def prices(update, context):

    try:
        arg = context.args[0]
    except IndexError:
        arg = ""

    if arg == "" or arg == "current":
        msg = get_last(CREDENTIALS)
    elif arg == "prev" or arg == "previous":
        msg = get_prev(CREDENTIALS)
    else:
        msg = "Invalid option: Use `/prices` or `/prices prev`"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )

def get_critter_msg(update, context, category):
    try:
        arg = context.args[0]
        name = context.args[1]
        name = re.sub("\s+", " ", " ".join(update.message.text.split(" ")[2:]))
    except IndexError:
        arg = ""
        name = ""

    if arg == "" or arg == "help" or name == "":
        msg = f"Usage:\n `/{category} info <name>` or `/{category} price <name>`"
    elif arg == "info":
        msg = format_info(get_info(name, category))
    elif arg == "price":
        msg = format_similar_names(get_similar_names(name, category), category)
    else:
        msg = f"Invalid option: Use `/{category} info <name>` or `/{category} price <name>`"

    return msg


def fish(update, context):
    msg = get_critter_msg(update, context, "fish")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )

def bug(update, context):
    msg = get_critter_msg(update, context, "bug")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)


    config = configparser.ConfigParser()
    config.read("config.ini")

    CREDENTIALS = config["DEFAULT"]["Credential"]
    TOKEN = config["DEFAULT"]["Token"]

    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    test_handler = CommandHandler("test", test)
    dispatcher.add_handler(test_handler)

    prices_handler = CommandHandler("prices", prices, pass_args=True)
    dispatcher.add_handler(prices_handler)

    fish_handler = CommandHandler("fish", fish, pass_args=True)
    dispatcher.add_handler(fish_handler)

    bug_handler = CommandHandler("bug", bug, pass_args=True)
    dispatcher.add_handler(bug_handler)

    updater.start_polling()

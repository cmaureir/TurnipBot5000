import re
import logging
import configparser

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

from lib.spreadsheet import get_last, get_prev, get_fossils, get_songs
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

def fossils(update, context):
    try:
        arg = context.args[0]
    except IndexError:
        arg = ""

    try:
        name = context.args[1]
        name = re.sub("\s+", " ", " ".join(update.message.text.split(" ")[2:]))
        name = name.lower().replace("á", "a")
    except:
        name = ""

    # Getting data
    missing, repeated, names = get_fossils(CREDENTIALS)

    if arg == "" or arg == "people" or arg == "help":
        msg = "People:\n\t"
        msg += ", ".join(names)
        msg += f"\n\nUsage:\n `/fossils need <name>` for the needed ones"
        msg += f"\n\nUsage:\n `/fossils have <name>` for the repeated ones"

    elif arg == "need":
        if name == "":
            msg = f"Usage:\n `/fossils need <name>`"
        else:
            if name not in missing:
                msg = f"Name '{name}' not found in: {', '.join(names)}"
            elif missing[name]:
                needed = []
                for x in missing[name]:
                    dino = x
                    people = []
                    for key, value in repeated.items():
                        if key == name:
                            continue
                        if x in value:
                            people.append(key)

                    if people:
                        dino = dino[:-1] + f" `({','.join(people)})`"
                    needed.append(dino)
                #msg = "\n".join(missing[name])
                msg = "\n".join(needed)

            else:
                msg = "No results"

    elif arg == "have":
        if name == "":
            msg = f"Usage:\n `/fossils have <name>`"
        else:
            if name not in repeated:
                msg = f"Name '{name}' not found in: {', '.join(names)}"
            elif repeated[name]:
                msg = "\n".join(repeated[name])
            else:
                msg = "No results"

    print(msg)
    msg = msg.replace(".", "\.")
    msg = msg.replace("(", "\(")
    msg = msg.replace(")", "\)")
    msg = msg.replace("-", "\-")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )


def songs(update, context):
    try:
        arg = context.args[0]
    except IndexError:
        arg = ""

    try:
        name = context.args[1]
        name = re.sub("\s+", " ", " ".join(update.message.text.split(" ")[2:]))
        name = name.lower().replace("á", "a")
    except:
        name = ""

    # Getting data
    missing, have, names = get_songs(CREDENTIALS)

    if arg == "" or arg == "people" or arg == "help":
        msg = "People:\n\t"
        msg += ", ".join(names)
        msg += "\n\nYou can order songs from the Nook Shopping App or ATM\n"
        msg += f"\n\nUsage:\n `/songs need <name>` for the needed ones"
        msg += f"\n\nUsage:\n `/songs have <name>` for the songs they have"

    elif arg == "need":
        if name == "":
            msg = f"Usage:\n `/songs need <name>`"
        else:
            if name not in missing:
                msg = f"Name '{name}' not found in: {', '.join(names)}"
            elif missing[name]:
                needed = []
                for x in missing[name]:
                    dino = x
                    people = []
                    for key, value in have.items():
                        if key == name:
                            continue
                        if x in value:
                            people.append(key)

                    if people:
                        dino = dino[:-1] + f" `({','.join(people)})`"
                    needed.append(dino)
                #msg = "\n".join(missing[name])
                msg = "\n".join(needed)

            else:
                msg = "No results"

    elif arg == "have":
        if name == "":
            msg = f"Usage:\n `/songs have <name>`"
        else:
            if name not in have:
                msg = f"Name '{name}' not found in: {', '.join(names)}"
            elif have[name]:
                msg = "\n".join(have[name])
            else:
                msg = "No results"

    print(msg)
    msg = msg.replace(".", "\.")
    msg = msg.replace("(", "\(")
    msg = msg.replace(")", "\)")
    msg = msg.replace("-", "\-")
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

    fossils_handler = CommandHandler("fossils", fossils, pass_args=True)
    dispatcher.add_handler(fossils_handler)

    songs_handler = CommandHandler("songs", songs, pass_args=True)
    dispatcher.add_handler(songs_handler)

    updater.start_polling()

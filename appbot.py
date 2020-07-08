#!/usr/bin/env python
"""
Home surveillance application
"""
import time

from lib.config import TOKEN_ID
from lib.telebot import Telebot

bot = Telebot(TOKEN_ID)

@bot.handler("/start")
def on_start():
    """
    command /start: start bot
    """
    bot.is_listen = True
    return bot.send_message("Bot start")


@bot.handler("/stop")
def on_stop():
    """
    command /stop: stop bot
    """
    bot.is_listen = False
    return bot.send_message("Bot stop")


@bot.handler("/status")
def on_status():
    """
    command /status: show bot status
    """
    return bot.send_message("Listening Motion run") \
        if bot.is_listen else bot.send_message("Listen Motion doesn't run")


@bot.handler("/photo")
def on_photo():
    """
    command /photo: take a photo
    """
    return bot.send_message("taking a photo")

@bot.handler("/video")
def on_video(*args):
    """
    command /video: record a video

    :param args: arguments of the bot's command
    """
    return bot.send_message("Recording start")


@bot.handler("/help")
def on_help():
    """
    command /help: show help
    :return: string
    """
    msg = "command usage:\n"
    msg += "\t/start : start the home monitoring system \n"
    msg += "\t/stop  : stop the home monitoring system\n"
    msg += "\t/show  : show the status of the monitoring system \n"
    msg += "\t/photo : take a picture\n"
    msg += "\t/video time=<delay> : records a video, argument time defines the duration of the recording\n"
    msg += "\t/clean : remove all files in video folder\n"
    msg += "\t/help  : show help\n"
    return bot.send_message(msg)


@bot.handler("/clean")
def on_clean():
    """
    command /clean: remove file in REGISTRATION_FOLDER
    """
    #return bot.send_message(camera.purge_records())
    return bot.send_message("cleaning ...")


print('I am listening ...')
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    del camera

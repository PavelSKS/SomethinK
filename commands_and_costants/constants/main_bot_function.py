import sys
import random
import sqlite3
import discord
import datetime
import schedule
import traceback

from discord.ext import commands, tasks

from constants import *
from command_message import *

client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')

connect = sqlite3.connect('data_base.db')
cursor = connect.cursor()


def check_channel(channel_id):
    return channel_id in WHITE_LIST_OF_CHANNEL or 0 in WHITE_LIST_OF_CHANNEL


def add_to_history(author_id, command_author, command, name, date, command_input):
    cursor.execute(
        f'''INSERT INTO command_history(user_id, author, discription, name, time, command)
        VALUES({author_id}, "{command_author}", "{command}", "{name}", "{date}", "{command_input}")''')
    connect.commit()
    return str(str(command_author) + '  -->  ' + str(command) + '  -->  ' + str(name) + '  **|**  at ' + str(date))


@client.event
async def on_ready():
    print('BOT connected')

    # server_id = ctx.message.guild.id
    # guild = ctx.message.guild
    # guild.id = int(server_id)

    names = ("REPORT SK", "HISTORY SK")

    # await guild.create_text_channel(names[0])
    # await guild.create_text_channel(names[1])

    # global ALERT_CHANNEL_ID, HISTORY_CHANNEL_ID
    # ALERT_CHANNEL_ID = discord.utils.get(ctx.guild.channels, name=names[0])
    # HISTORY_CHANNEL_ID = discord.utils.get(ctx.guild.channels, name=names[1])

    await client.change_presence(status=discord.Status.online, activity=discord.Game("cлежку за вами <3"))

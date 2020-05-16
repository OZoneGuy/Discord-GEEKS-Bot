"""
The main discord bot script.
"""

import json
from datetime import datetime

from discord.ext import commands
from welcome_cog import Welcome

VERSION = "0.15.5.20 A"

config = json.load(open("config.json"))

# channel IDs
DEV_CHANNEL = 385506783919079425


def write_log(text: str):
    """
    Write 'str' as a log into the log file.
    """
    text = str(datetime.now()) + " - " + text + "\n"
    f_log = open("GEEK.log", "a+")
    f_log.write(text)
    f_log.close()


# bot client
bot: commands.Bot = commands.Bot(command_prefix='$')


# on ready function - logs ready time
@bot.listen()
async def on_ready():
    """
    Called when the bot is ready.
    """
    print("TheGeek is ready.")
    bot.add_cog(Welcome(bot))
    write_log("Ready.")


async def in_dev(ctx: commands.Context) -> bool:
    '''
    checks if message came from dev
    '''
    return ctx.channel.id == DEV_CHANNEL


@bot.command()
@commands.check(in_dev)
async def status(ctx):
    """
    A command used to check the status of the bot.
    """
    print("test")
    await ctx.channel.send(content="Up and Running. Version: " + VERSION,
                           delete_after=3)


bot.run(config['token'])

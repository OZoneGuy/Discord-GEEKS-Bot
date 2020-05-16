"""
The main discord bot script.
"""

import json

from discord.ext import commands

from bot_utils import write_log

VERSION = "0.15.5.20 A"

config = json.load(open("config_test.json"))

# channel IDs
DEV_CHANNEL = 385506783919079425


# bot client
bot: commands.Bot = commands.Bot(command_prefix='$')


# on ready function - logs ready time
@bot.listen()
async def on_ready():
    """
    Called when the bot is ready.
    """
    print("TheGeek is ready.")
    bot.load_extension('welcome_cog')
    await bot.get_cog('Welcome').load_ids()
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


@bot.command()
async def reloadWelcome(ctx):
    bot.reload_extension('welcome_cog')
    await bot.get_cog('Welcome').load_ids()


bot.run(config['token'])

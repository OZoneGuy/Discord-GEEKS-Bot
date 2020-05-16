import discord
from discord.ext import commands
import json
from datetime import datetime

version = "0.19.10.19 A"

config = json.load(open("config.json"))

# channel IDs
reg_channel = 635285850015531028
dev_channel = 385506783919079425
role_channel = 635285966218592266
general_channel = 378272844313919500


# takes a text and logs into file with timestamp
def write_log(text: str):
    text = str(datetime.now()) + " - " + text + "\n"
    f = open("GEEK.log", "a+")
    f.write(text)
    f.close()

# bot client


bot: commands.Bot = commands.Bot(command_prefix='$')


# on ready function - logs ready time
@bot.listen()
async def on_ready():
    print("TheGeek is ready.")
    write_log("Ready.")


@bot.listen()
async def on_message(message: discord.Message):
    '''
    Called when a user sends a message in a chat the bot can access,
    server channels, DMs, etc.
    Not used for anything atm
    '''
    if message.author == bot.user:
        return
        pass


async def in_dev(ctx: commands.Context) -> bool:
    '''
    checks if message came from dev
    '''
    return ctx.channel.id == dev_channel


@bot.command()
@commands.check(in_dev)
async def hello(ctx):
    print("test")
    await ctx.channel.send(content="It's Alive!!!", delete_after=3)
    pass

bot.run(config['token'])

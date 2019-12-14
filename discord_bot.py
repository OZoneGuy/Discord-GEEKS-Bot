import discord
from discord.ext import commands
import json
import sql_handler
import sheets_interface
import random
from emoji import emojize, demojize
from datetime import datetime

version = "0.19.10.19 A"

config = json.load(open("config.json"))

# channel IDs
reg_channel = 635285850015531028
dev_channel = 385506783919079425
role_channel = 635285966218592266
general_channel = 378272844313919500

# messages ids
registration_message_id : int
role_message_id : int

# role constants
roles_dic =   { ':Japan:':                      487415117361971200, # anime
                ':pick:':                       570307869279518720, # minecraft
                ':large_blue_diamond:':         554029029905137676, # tetris
                ':VS_button:':                  487415401085403157, # smash
                ':paw_prints:':                 488887610882916352, # pokemon
                ':flower_playing_cards:':       487415696507142164, # TCG
                ':trophy:':                     619372177757831168, # eSports
                ':game_die:':                   626161640768798730, # Boardgames
                ':crossed_swords:':             619372523754094602, # MMO
                ':top_hat:':                    619371680992591882, # tabletop
                ':video_game:':                 487415401131540490, # video games
                ':dragon_face:':                487415117420429312, # DnD

                'events':                       00000000000,      # needs a new tag
                'film':                         0000000000,        # needs a new tag
                'pokemon_go':                   00000000000,  # needs a new tag

                # need to change to emojis
                ':detective:':                  406508496314564608,
                ':graduation_cap:':             403701567305285633}

# Strings
not_reg_msg     = "You are not registered {}. Please finish the google form in the pinned message."
reg_msg         = "Welcome {}!"

register_message_text   = """Welcome to the McMaster Geeks Discord server!
If you would like access to the channels,(else why would you be here?) you need to finish the google form linked below then come back here and add a :mortar_board: reaction to this message. I will take care of the rest!

If you are a guest, then add the :spy: reaction to get access!

One more thing! To distinguish yourself from other and help others know you better, you might want to get a tag! Go to #role-channel Just simply add the reaction that matches the tag you want and voila!


> Joining our server has never been easier! - @OzoneGuy#2203
You see this ↑
So if anything happens make sure to bother him. He has no friends and likes the attention!
"""


role_message_text : str = """Add a reaction to get a tag. Remove the reaction to lose the tag.
    :flag_jp: Anime
    :pick: Minecraft
    :vs: Smash
    :feet: Pokémon
    :large_blue_diamond: Tetris
    :game_die: Board Games
    :tophat:  Tabletop
    :dragon_face: DnD
    :flower_playing_cards: TCG
    :trophy: eSports
    :video_game: Videogames
    :crossed_swords: MMO"""

# intro_messages
intro_messages = [
    "{} has joined the server! It's super effective.",
    "Brace yourselves. {} just joined the server.",
    "{} joined. You must construct additional pylons.",
    "A {} has spawned in the server.",
    "{} has joined. Can I get a heal?",
    "{} just slid into the server.",
    "Roses are red, violets are blue, {} joined this server with you",
    "Hey! Listen! {} has joined!",
    "We've been expecting you {}",
    "{}. Hina is here",
    "Hello. Is it {} you're looking for?",
    "{} just arrived. Seems OP - please nerf",
    "Ermagherd. {} is here.",
    "It's dangerous to go alone, take {}!",
    "{} has joined the battle bus.",
    "{} just joined the party.",
    "Welcome, {}. Stay awhile and listen.",
    "Cheers, love! {} is here!",
    "Where is {}? In the server!",
]

# takes a text and logs into file with timestamp
def write_log(text: str):
    text = str(datetime.now()) + " - " + text + "\n"
    f = open("GEEK.log", "a+")
    f.write(text)
    f.close()

#bot client
bot : commands.Bot = commands.Bot(command_prefix='$')


# on ready function - logs ready time
@bot.listen()
async def on_ready():
    print("TheGeek is ready.")
    write_log("Ready.")

@bot.listen()
async def on_message(message: discord.Message):
    '''
    Called when a user sends a message in a chat the bot can access, server channels, DMs, etc.
    Not used for anything atm
    '''
    if message.author == bot.user:
        return
        pass


# add role depending on reaction to message
@bot.listen()
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    '''
    Only does something when users react to a specific message
    Removes user role depending on reaction only if they are registered/students
    '''
    # gets text form of emoji
    # if it a unicode emoji uses `emoji` library to get text form
    # else discord provides the name
    emoji_name = demojize(payload.emoji.name) if payload.emoji.is_unicode_emoji() else payload.emoji.name

    guild: discord.Guild = bot.get_guild(payload.guild_id)
    member: discord.Member = guild.get_member(payload.user_id)
    channel: discord.TextChannel = bot.get_channel(payload.channel_id)
    role: discord.Role = guild.get_role(roles_dic[emoji_name])

    if payload.message_id == role_message_id:
        # remove member role
        await member.remove_roles(role)
        # print message and delete after 3 seconds
        await channel.send(content="Removed {} tag. {}.".format(role.name, member.mention), delete_after=3)
        write_log("Removed {} from {}".format(role.name, member.name))

    if payload.message_id == registration_message_id:
        await channel.send(content="Not sure what you are trying to. For assistance please contact @ZoneGuy.", delete_after=3)

@bot.listen()
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    '''
    Only does something when users react to a specific message
    Gives user role depending on reaction only if they are registered/students
    '''
    # ignores everything if user is bot
    if payload.user_id == bot.user.id:
        return
    # gets text form of emoji
    # if it a unicode emoji uses `emoji` library to get text form
    # else discord provides the name
    emoji_name : str = demojize(payload.emoji.name) if payload.emoji.is_unicode_emoji() else payload.emoji.name
    guild:discord.Guild           = bot.get_guild(payload.guild_id)
    member : discord.Member       = guild.get_member(payload.user_id)
    channel : discord.TextChannel = bot.get_channel(payload.channel_id)
    role : discord.Role = guild.get_role(roles_dic[emoji_name])

    if payload.message_id == role_message_id:
        if "mcmaster student" in [role_string.name.lower() for role_string in member.roles]:
            if role in member.roles:
                await channel.send("You already have this role! Remove the reaction to remove your role.", delete_after=3)
                write_log("{} tried to take already owned role, {}".format(member.name, role.name))
            else:
                # add member role
                try:
                    await member.add_roles(role)
                except:
                    await channel.send(content="Oops! Something went wrong. We will investigate it shortly", delete_after=3)
                    write_log("Failed to give role. Emoji name: {}, Role ID: {}".format(emoji_name, roles_dic[emoji_name]))
                    # print message and delete after 3 seconds
                    await channel.send("Added {} tag. {}.".format(role.name, member.mention), delete_after=3)
                    write_log("Given {} tag to {}.".format(role.name, member.name))
        else:
            await channel.send(content="You need to register first! Go to #sign-up and register.", delete_after=5)
            message : discord.Message = channel.fetch_message(payload.message_id)
            await message.remove_reaction(emojize(emoji_name), member)


    # registration
    if payload.message_id == registration_message_id:
        # student
        if role.id == 403701567305285633:
            if not await register(channel, member, role):
                channel.fetch_message(payload.message_id).remove_reaction(emojize(emoji_name), member)
        # guest
        if role.id == 406508496314564608:
            await add_guest(channel , member, role)


async def register(channel: discord.TextChannel, member: discord.Member, role: discord.Role) -> bool:
    '''
    Gives user Student tag if they have registered on google form
    '''
    write_log("Attempting to register {}".format(member.display_name))
    if 403701567305285633 in [role.id for role in member.roles]:
        await channel.send(content="You are already registered.", delete_after=3)
        write_log("{} already has student tag".format(member.display_name))
        return True
    if sql_handler.is_registered(member.name, member.discriminator):
        await member.add_roles(role)
        await channel.send(content=reg_msg.format(member.mention), delete_after=3)
        write_log("Successfully given {} student tag".format(member.display_name))
        bot.get_channel(general_channel).send(random.choice(intro_messages).format(member.mention))
        return True
    else:
        await channel.send(content=not_reg_msg.format(member.mention), delete_after=3)
        write_log("{} is not registered.".format(member.display_name))
        return False

async def add_guest(channel: discord.TextChannel, member: discord.Member, role: discord.Role):
    '''
    Give user `Guest` tag
    '''
    write_log("Attempting to give guest tag to {}".format(member.display_name))
    if 403701567305285633 in [role.id for role in member.roles]:
        await channel.send(content="You are registered, you don't the guest tag.", delete_after=3)
        write_log("{} already has student tag.".format(member.display_name))
        return
    if 406508496314564608 in [role.id for role in member.roles]:
        await channel.send(content="You already have `Guest` role.", delete_after=3)
        write_log("{} already has guest tag")
        return
    await member.add_roles(role)
    await channel.send(content="Welcome {}. You are a guest now!", delete_after=3)
    write_log("Given {} guest tag.".format(member.display_name))

async def welcome_message(message: discord.Message):
    '''
    Creates registration and role messages and stores their ids
    '''
    embed = discord.Embed(title="Sign up form.",
                          url="https://goo.gl/forms/phEbKvQzTi6MlIQ12")

    # send reg and role messages ad get them to add reactions
    await bot.get_channel(reg_channel).purge()
    await bot.get_channel(role_channel).purge()
    registration_message : discord.Message = await bot.get_channel(reg_channel).send(content=register_message_text, embed=embed)
    role_message : discord.Message = await bot.get_channel(role_channel).send(content=role_message_text)

    dict_keys = list(roles_dic.keys())

    # add reactions to role message
    for i in range(12):
        await role_message.add_reaction(emojize(dict_keys[i]))
        pass

    # add reactions to registration message
    for i in range(15, 17):
        await registration_message.add_reaction(emojize(dict_keys[i]))

    # save messages ids
    global registration_message_id
    global role_message_id
    registration_message_id = registration_message.id
    role_message_id = role_message.id
    await message.delete()
    pass


async def in_dev(ctx: commands.Context) -> bool:
    '''
    checks if message came from dev
    '''
    return ctx.channel.id == dev_channel


@bot.command()
@commands.check(in_dev)
async def dewit(ctx: commands.Context):
    '''
    executes order 'welcome'
    '''
    await welcome_message(ctx.message)
    pass


@bot.command()
@commands.check(in_dev)
async def hello(ctx):
    print("test")
    await ctx.channel.send(content="It's Alive!!!", delete_after=3)
    pass

bot.run(config['token'])

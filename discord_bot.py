import discord
import json
import sql_handler
import sheets_interface
from emoji import emojize, demojize
from datetime import datetime

version = "0.8.10.19 A"

config = json.load(open("config_test.json"))

# channel IDs
reg_channel = 406292711646167045
dev_channel = 385506783919079425
com_channel = 520680784949018639

# role constants
# TODO get actual message id
registration_message_id : int = 00000000
role_message_id : int = 0000000
# TODO replace keys with emojis
roles_dic =   { ':Japan:':                      487415117361971200, # anime
                ':pick:':                       570307869279518720, # minecraft
                ':large_blue_diamond:':         554029029905137676, # tetris
                ':VS_button:':                  487415401085403157, # smash
                ':paw_prints:':                 488887610882916352, # pokemon
                ':flower_playing_cards:':       448741569650714216, # TCG
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

intro_message   = """Welcome to the McMaster Geeks Discord server!
If you would like access to the channels,(else why would you be here?) you need to finish the google form linked below then come back here and add a reaction to the message below. I will take care of the rest!

One more thing! To distinguish yourself from other and help others know you better, you might want to get a tag! Just simply add the reaction that matches the tag you want and voila!

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
    :crossed_swords: MMO

> Joining out server has never been easier! - @OzoneGuy#2203
You see this ↑
So if anything happens make sure to bother him. He likes the attention!
"""

register_message_text : str = """Registration reaction here!"""

role_message_text : str = "Role reaction here!"


# takes a text and logs into file with timestamp
def write_log(text: str):
    text = str(datetime.now()) + " - " + text + "\n"
    f = open("GEEK.log", "a+")
    f.write(text)
    f.close()

#bot client
client : discord.Client = discord.Client()

# on ready function - logs ready time
@client.event
async def on_ready():
    print("TheGeek is ready.")
    write_log("Ready.")

@client.event
async def on_message(message: discord.Message):
    '''
    Called when a user sends a message in a chat the bot can access, server channels, DMs, etc.
    Used to react to messages asking for registration.
    '''
    if message.author == client.user:
        return
    if '!demo' in message.content:
        await welcome_message(message)
        pass
    if message.channel.id == dev_channel:
        # no dev commands yet
        pass
    # Used for registering users
    elif message.channel.id == reg_channel:
        '''
        handles commands on register channel
        '''
        # attempts to register user
        if "!dewit" in message.content:
            welcome_message(message)


# add role depending on reaction to message
@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    '''
    Only does something when users react to a specific message
    Removes user role depending on reaction only if they are registered/students
    '''
    # gets text form of emoji
    # if it a unicode emoji uses `emoji` library to get text form
    # else discord provides the name
    emoji_name = demojize(payload.emoji.name) if payload.emoji.is_unicode_emoji() else payload.emoji.name

    guild: discord.Guild = client.get_guild(payload.guild_id)
    member: discord.Member = guild.get_member(payload.user_id)
    channel: discord.TextChannel = client.get_channel(payload.channel_id)
    role: discord.Role = guild.get_role(roles_dic[emoji_name])

    if payload.message_id == role_message_id:
        # remove member role
        await member.remove_roles(role)
        # print message and delete after 3 seconds
        await channel.send(content="Removed {} tag. {}.".format(role.name, member.mention), delete_after=3)
        write_log("Removed {} from {}".format(role.name, member.name))

    if payload.message_id == registration_message_id:
        await channel.send(content="Not sure what you are trying to. For assistance please contact @ZoneGuy.", delete_after=3)

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    '''
    Only does something when users react to a specific message
    Gives user role depending on reaction only if they are registered/students
    '''
    # ignores everything if user is bot
    if payload.user_id == client.user.id:
        return

    # gets text form of emoji
    # if it a unicode emoji uses `emoji` library to get text form
    # else discord provides the name
    emoji_name = demojize(payload.emoji.name) if payload.emoji.is_unicode_emoji() else payload.emoji.name

    guild:discord.Guild           = client.get_guild(payload.guild_id)
    member : discord.Member       = guild.get_member(payload.user_id)
    channel : discord.TextChannel = client.get_channel(payload.channel_id)
    role : discord.Role = guild.get_role(roles_dic[emoji_name])

    if payload.message_id == role_message_id:
        if role in member.roles:
            await channel.send("You already have this role! Remove the reaction to remove your role.", delete_after=3)
            write_log("{} tried to take already owned role, {}".format(member.name, role.name))
        else:
            # add member role
            await member.add_roles(role)
            # print message and delete after 3 seconds
            await channel.send("Added {} tag. {}.".format(role.name, member.mention), delete_after=3)
            write_log("Given {} tag to {}.".format(role.name, member.name))

    # registration
    if payload.message_id == registration_message_id:
        # student
        if role.id == 403701567305285633:
            await register(channel, member, role)
        # guest
        if role.id == 406508496314564608:
            await add_guest(channel , member, role)


async def register(channel: discord.TextChannel, member: discord.Member, role: discord.Role):
    '''
    Gives user Student tag if they have registered on google form
    '''
    write_log("Attempting to register {}".format(member.display_name))
    if 403701567305285633 in [role.id for role in member.roles]:
        await channel.send(content="You are already registered.", delete_after=3)
        write_log("{} already has student tag".format(member.display_name))
        return
    if sql_handler.is_registered(member.display_name, member.user_disc):
        await member.add_roles(role)
        await channel.send(content=reg_msg.format(member.mention), delete_after=3)
        write_log("Successfully given {} student tag".format(member.display_name))
    else:
        await channel.send(content=not_reg_msg.format(member.mention), delete_after=3)
        write_log("{} is not registered.".format(member.display_name))

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
    embed = discord.Embed(title="Sign up form.",
                          url="https://goo.gl/forms/phEbKvQzTi6MlIQ12")
    await message.channel.send(content=intro_message, embed=embed)

    # send reg and role messages ad get them to add reactions
    registration_message : discord.Message = await message.channel.send(content=register_message_text)
    role_message : discord.Message = await message.channel.send(content=role_message_text)

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



client.run(config['token'])

import discord
import json
import sql_handler
import sheets_interface
from datetime import datetime



reg_channel = 406292711646167045
dev_channel = 385506783919079425
com_channel = 520680784949018639

version = "2.9.19 B"

@client.event
async def on_ready():
    print('Starting Discord Bot.\tVersion: {}'.format(version))
    print('Logged in as {0.user}'.format(client))
    pass


@client.event
async def on_message(message):

    #ignores messages sned by the bot
    if message.author is client.user:
        return

    #adds to the count of total messages made by user for level up system
    # if message.channel.id == dev_channel:
    sql_handler.add_message(message.author.id)
    #checks if user is ready for a level up
    if sql_handler.is_lvl_up(message.author.id):
        print('new level')
        sql_handler.lvl_up(message.author.id)
        if sql_handler.get_level(message.author.id) >= 5:
            await level_up(message)

    #registers the user
    if message.content.startswith('!register') and (message.channel.id == reg_channel or message.channel.id == com_channel or message.channel.id == dev_channel):
        await register(message)
    #adds tag to the user
    if message.content.startswith('!tag ') and (message.channel.id == com_channel or message.channel.id == dev_channel):
        await give_tag(message)

    #gives all commands user can use
    if message.content.startswith('!botcommands'):
        await message.channel.send( 'To register use:\n\t`!register`\nTo get a tag use(Only available in the `#botcommands` channel):\n\t`!tag TAG_NAME`\nAvailable tags are:\n\tAnime\n\tDND\n\tSmash\n\tPokemon\n\tMTG\n\tVideo Games\n\nIf there are any issues please contact the mods or OZoneGuy.')

#    if message.channel.id == dev_channel and contains_im(message.content):
#        print(contains_im(message.content))
#        if random.random()>0.2:
#            await message.channel.send( 'Hello {0}. I am The GEEKS Bot!'.format(contains_im(message.content)))


    #used for testint
    if message.content.startswith('!hello') and message.channel.id == dev_channel:
        await message.channel.send( 'Hello to you too!')
    if message.content.startswith('test') and message.channel.id == dev_channel:
        print('updating DB')
        sheets_interface.main()

@client.event
async def on_member_join(member):
    await message.channel.send(member, "Welcome to the `McMaster GEEKS` discord server!\n To register and gain access to the server please complete the `google form` linked below. Then you can use the `!register` command to register!\nhttps://goo.gl/forms/phEbKvQzTi6MlIQ12")

# updates user database using the sheets sheets_interface script
# checks if user is registered in the database
# if the user is not found it will send an error message
async def register(message):
    tries = 0
    while tries < 3:
        sheets_interface.main()
        if sql_handler.is_registered(message.author.name, message.author.discriminator):
            role = discord.utils.get(message.guild.roles, name='McMaster Student')
            await message.author.add_roles(role)
            await message.channel.send( 'Enjoy your stay :grinning:')
            print("Registered {}.".format(message.author.name))
            return
        time.sleep(0.5)
        tries+=1

    await message.channel.send( 'You need to register first , https://goo.gl/forms/phEbKvQzTi6MlIQ12 . \n If you have already registered then wait a few minutes and try again, if the issue still persists, then contact OZoneGuy or the server mods to resolve the issue.')
    return


allowed_roles = ['video games', 'mtg', 'pokemon', 'smash', 'dnd', 'anime', 'minecraft']
roles_dic =   { 'anime':        487415117361971200,
                'dnd':          487415117420429312,
                'minecraft':    570307869279518720,
                'tetris':       554029029905137676,
                'smash':        487415401085403157,
                'pokemon':      488887610882916352,
                'mtg':          487415696507142164,
                'video games':  487415401131540490}

async def give_tag(message):
    role_string = message.content[5:].lower()
    role = message.guild.get_role(roles_dic[role_string])
    author = message.author
    if not (role_string in allowed_roles):
        await message.channel.send( 'You do not have permission to get this role.')
        return
    if "McMaster Student".lower() in [y.name.lower() for y in author.roles]:
        if role is not None:
            if role in author.roles:
                await message.channel.send( 'You already have this tag!')
                return
            await author.add_roles(role)
            await message.channel.send(
                                      'Enjoy your new tag :grinning: {0.author.mention}'.format(message))

            return
        else:
            await message.channel.send( 'Role does not exist.')
            return
    else:
        await message.channel.send( 'You need to register first. Please use `!register`.')
        return

async def level_up(message):
    message_cnt = sql_handler.messages_req_for_lvl(sql_handler.get_level(message.author.id)) - sql_handler.get_messages(message.author.id)
    await message.channel.send( 'Congrats {} for reaching level {}! Only {} messages more to go.'.format(message.author.mention, sql_handler.get_level(message.author.id), message_cnt))

def contains_im(text):
    if 'I am' in text:
        word = text.split("I am", 1)[1].split(" ")[1]
        return word

    if "I'm" in text:
        word = text.split("I'm", 1)[1].split(" ")[1]
        return word

    if "Im" in text:
        word = text.split("Im", 1)[1].split(" ")[1]
        return word

    if "im" in text:
        word = text.split("im", 1)[1].split(" ")[1]
        return [True, word]

client.run(config['token'])

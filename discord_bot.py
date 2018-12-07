import discord
import json
import sql_handler
import sheets_interface
config = json.load(open('config.json'))

client = discord.Client()

forbidden_roles = ['PRISON WARDENS', 'GEEKS Exec', 'Vault Exec', 'Community Moderator', 'Seasoned Veterans',
                   'Vault Hunters', 'McMaster GEEKS Role Bot', 'Bot Army']


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    pass


@client.event
async def on_message(message):
    if message.author is client.user:
        return

    # real is is 406292711646167045
    #delvelopement channel is 385506783919079425

    #registers the user
    if message.content.startswith('!register') and (message.channel.id == '406292711646167045' or message.channel.id == '520680784949018639'):
        await register(message)
    #adds tag to the user
    if message.content.startswith('!tag ') and (message.channel.id == '520680784949018639'):
        await give_tag(message)

    #gives all commands user can use
    if message.content.startswith('!help') and (message.channel.id == '520680784949018639' or message.channel.id == '385506783919079425'):
        await client.send_message(message.channel, 'To register use:\n\t\'!register\'\nTo get a tag use:\n\t\'!tag TAG_NAME\'\nAvailable tags are:\n\tAnime\n\tDND\n\tSmash\n\tPokemon\n\tMTG\n\tVideo Games\n\nIf there are any issues please contact the mods or OZoneGuy.')

    if message.content.startswith('!hello') and message.channel.id == '385506783919079425':
        await client.send_message(message.channel, 'Hello to \n you too!')
    if message.content.startswith('test') and message.channel.id == '385506783919079425':
        print('hello')
        sheets_interface.main

# TODO: implement on error function to log the error and prompt user to contact me or moderator
# @client.event
# async def on_error(event, *args, **kwargs):
#     pass

async def register(message):
    sheets_interface.main
    if sql_handler.is_registered(author.name):
        await client.add_roles(author, role)
        await client.send_message(message.channel, 'Enjoy your stay :grinning:')
        return
    else:
        await client.send_message(message.channel, 'You need to register first , https://goo.gl/forms/phEbKvQzTi6MlIQ12 . \n If you have already registered then wait a few minutes and try again, if the issue still persists, then contact OZoneGuy or the server mods to resolve the issue.')
        sheets_interface.main
        return

async def give_tag(message):
    role_string = message.content[5:]
    author = message.author
    role = discord.utils.get(message.server.roles, name=role_string)
    if role_string in forbidden_roles:
        await client.send_message(message.channel, 'You do not have permission to get this role.')
        return
    if "McMaster Student".lower() in [y.name.lower() for y in author.roles]:
        if role is not None:
            if role in author.roles:
                await client.send_message(message.channel, 'You already have this tag!')
                return
            await client.add_roles(author, role)
            await client.send_message(message.channel,
                                      'Enjoy your new tag :grinning: {0.author.mention}'.format(message))

            return
        else:
            await client.send_message(message.channel, 'Role does not exist.')
            return
    else:
        await client.send_message(message.channel, 'You need the required tag first.')
        return


client.run(config['token'])

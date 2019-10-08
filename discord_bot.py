import discord
import json
import sql_handler
import sheets_interface
import emoji
from datetime import datetime



# channel IDs
reg_channel = 406292711646167045
dev_channel = 385506783919079425
com_channel = 520680784949018639

# role constants
# TODO get actual message id
role_message = 0000000
# TODO replace keys with emojis
roles_dic =   { ':flag_jp:':                    487415117361971200, #need to ask Atom about each reaction
                ':pick:':                       570307869279518720,
                ':large_blue_diamond:':         554029029905137676,
                ':vs:':                         487415401085403157,
                ':feet:':                       488887610882916352,
                ':flower_playing_cards:':       448741569650714216,
                ':trophy:':                     619372177757831168,
                ':game_die:':                   626161640768798730,
                'MMO':                          619372523754094602,
                'table_top':                    619371680992591882,
                'video games':                  487415401131540490,
                'dnd':                          487415117420429312,

                # used by !... commands to get role id
                'guest':                        406508496314564608,
                'student':                      403701567305285633}

# Strings
not_reg_msg     = "You are not registered {}. Please finish the google form in the pinned message."
reg_msg         = "Welcome {}!"

# takes a text and logs into file with timestamp
def write_log(text: str):
    text = str(datetime.now()) + " - " + text + "\n"
    f = open("GEEK.log", "a+")
    f.write(text)
    f.close()
    pass

#bot client
client = discord.Client() # type: discord.Client

# on ready function - logs ready time
@client.event
async def on_ready():
    print('Starting Discord Bot.\tVersion: {}'.format(version))
    write_log("Ready.")
    pass

@client.event

@client.event
        else:



async def register(message: discord.Message):
    '''
    Gives user Student tag if they have registered on google form
    '''
    # log action start
    write_log(format("Registering {} ...", message.author.name))    
    # check if user registered
    if (is_registered(message.author.name, message.author.discriminator)):
        role = message.guild.get_role(roles_dic['student']) # type: discord.Role
        message.author.add_role(role) # add role
        write_log(format("Successfully registered {} !", message.author.name)) # log result
        message.channel.send(content=reg_msg.format(message.author.mention)).delete(delay=3) # notify user success and delete notify message after 3 seconds
        message.delete(delay=0.5) # delete user message
    else:
        write_log(format("Failed to register {}!", message.author.name)) # log result (failure)
        message.channel.send(content=not_reg_msg.format(message.author.mention)).delete(delay=3) # notify user of failure then delete notify message
        message.delete(delay=0.5) # delete user message
    pass

client.run(config['token'])

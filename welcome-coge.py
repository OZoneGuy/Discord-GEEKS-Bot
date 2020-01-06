from discord.ext import commands # commands classes
import discord

import sql_handler # sql interface

import json
from emoji import emojize, demojize

reg_channel_id : int
role_channel_id : int

register_message_id : int
role_message_id : int

role_dict : dict

class Welcome(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

        load_ids()
        pass

    async def load_ids():
        '''
        Loads role_message_id, register_message_id, reg_channel, role_channel from json file
        '''
        with open('config.json', 'rw') as j_file :
            # get json data
            reg_data       = json.load(j_file)['reg_data']
            global role_channel_id
            global reg_channel_id
            global register_message_id
            global role_message_id
            global role_dict

            # get roles/emoji dict
            role_dict = reg_data['roles_emoji_dict']

            # get channel ids
            reg_channel_id = reg_data['reg_channel_id']
            role_channel_id = reg_data['role_channel_id']

            # check message id
            register_message_id = reg_data['reg_message_id']

            # check if it is 0, if it is 0 then it needs initialization
            if register_message_id is 0:
                # get relevant channels
                reg_channel :  discord.TextChannel = await self.bot.get_channel(reg_data['reg_channel_id'])
                role_channel : discord.TextChannel = await self.bot.get_channel(reg_data['role_channel_id'])

                # delete all messages
                reg_channel.purge()
                role_channel.purge()

                # prepare embedded link for reg message
                embed : discord.Embed = discord.Embed(title="Sign up form.",
                                                      url="https://goo.gl/forms/phEbKvQzTi6MlIQ12")

                # send messages and get messages for future references
                reg_message :  discord.Message = await reg_channel.send(content=get_message_from_json('reg_message').format(
                    self.bot.fetch_user(415154371924590593).mention)
                                                                        , embed=embed)
                role_message : discord.Message = await role_channel.send(content=get_message_from_json('role_message'))

                # get a list of emojis
                emoji_dict_keys = list(reg_data['roles_emoji_dict'].keys())

                # add reactions to role message
                for i in range(12):
                    await role_message.add_reaction(emojize(emoji_dict_keys[i]))
                    pass

                # add reactions to registration message
                for i in range(15, 17):
                    await role_message.add_reaction(emojize(emoji_dict_keys[i]))
                    pass

                # save ids to dictionary to be save in json file
                reg_data['reg_message_id']  = reg_message.id
                reg_data['role_message_id'] = role_message.id

                # save data to dictionary and json file
                j_data['reg_data'] = reg_data
                json.dump(j_data, 'config.json')
                pass

            role_channel_id = reg_data['role_channel_id']
            role_message_id = reg_data['role_message_id']
        pass

    # get message string from json file
    def get_message_from_json(data : str) -> str:
        messages : dict = json.load(open('messages.json'))
        return messages[data]
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(payload: RawReactionActionEvent):
        '''
        Only does something when users react to a specific message
        Gives user role depending on reaction only if they are registered/students
        '''
        # ignore everything is user is bot
        if payload.user_id == self.bot.user.id:
            return

        emoji :   str                 = demojize(payload.emoji.name)
        guild :   discord.Guild       = self.bot.get_guild(payload.guild_id)

        member :  discord.Member      = guild.get_member(payload.user_id)
        channel : discord.TextChannel = self.bot.get_channel(payload.channel_id)

        # will throw an error if the emoji doesn't exist in the dictionary
        try:
            role : discord.Role = guild.get_role(role_dict[emoji])
        except Exception as e:
            return

        # handles reactions to reg message
        if payload.message_id == reg_message_id:
            # the user wants to get student tag
            if emoji == ":graduation_cap:":
                register(channel, member, role, emoji)
                pass
            # the user wants to get guest tag
            if emoji == ":spy:":
                await add_guest(channel, member)
                pass
            pass

        if payload.message_id == role_message_id:
            await give_role(channel, member, role)
            pass
        pass

    async def register(channel : discord.TextChannel, member : discord.Member, emoji : str) -> bool:
        """
        Checks if the user is registered.
        If they are give them student role and send affirmative message, else send them negative message.
        """
        if sql_handler.is_registered(member.name, member.user.discriminator):
            await member.add_roles(self.bot.get_role(role_dict[':graduation_cap:'])) # give role
            await channel.send(content=get_message_from_json("reg_suc_message").format(member.mention), delete_after=3) # send a confirmation message
            pass
        else:
            await channel.send(content=get_message_from_json("not_reg_message").format(member.mention), delete_after=3) # send a negative message
            channel.fetch_message(payload.message_id).remove_reaction(emojize(emoji), member) # remove user reaction from message
        pass

    async def add_geust(channel : discord.TextChannel, member : discord.Member):
        await member.add_roles(self.bot.get_tole(role_dict[':detective:'])) # give guest role
        await channel.send(content=get_message_from_json("guest_message").format(member.mention), delete_after=3)
        pass

    async def give_role(channel : discord.TextChannel, member : discord.Member, role : discord.Role):
        """
        Gives the member a role/tag.
        First it checks if the member is register, have the mcmaster student tag.
        """
        if not "mcmaster student" in [role.name.lower for role in member.roles]:
            await channel.send(content=get_messge_from_json("role_fail"), delete_after=3)
            pass
        else:
            if not role in [role for role in member.role]:
                await member.add_roles(role)
                await channel.send(content=get_message_from_json("role_suc").format(member.mention), delete_after=3)
                pass
            else:
                await channel.send(content=get_message_from_json("role_exit"), delte_after=3)
                pass
        pass
    pass

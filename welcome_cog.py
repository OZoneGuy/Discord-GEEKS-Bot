from discord.ext import commands  # commands classes
import discord

import sql_handler  # sql interface

import json
from emoji import emojize, demojize


class Welcome(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

        self.load_ids()
        pass

    async def load_ids(self):
        '''
        Loads role_message_id, register_message_id, reg_channel_id,
        role_channel_id from json file
        '''
        with open('config_test.json', 'rw') as j_file:
            # get json data
            j_data = json.load(j_file)
            reg_data = j_data['reg_data']

            # get roles/emoji dict
            self.role_dict = reg_data['roles_emoji_dict']

            # get channel ids
            self.reg_channel_id = reg_data['reg_channel_id']
            self.role_channel_id = reg_data['role_channel_id']

            # check message id
            self.register_message_id = reg_data['reg_message_id']

            # check if register_message_id is 0, if it is 0 then it needs
            # initialisation
            if self.register_message_id == 0:
                # get relevant channels
                reg_channel: discord.TextChannel = await self.bot.get_channel(
                    self.reg_channel_d)
                role_channel: discord.TextChannel = await self.bot.get_channel(
                    self.role_channel_id)

                # delete all messages
                reg_channel.purge()
                role_channel.purge()

                # prepare embedded link for reg message
                embed: discord.Embed = discord.Embed(
                    title="Sign up form.",
                    url="https://goo.gl/forms/phEbKvQzTi6MlIQ12")

                # send messages and get messages for future references
                reg_message: discord.Message = await reg_channel.send(
                    content=self.get_message_from_json('reg_message').format(
                        self.bot.fetch_user(415154371924590593).mention),
                    embed=embed)
                role_message: discord.Message = await role_channel.send(
                    content=self.get_message_from_json('role_message'))

                # get a list of emojis
                emoji_dict_keys = list(self.role_dict)

                # add reactions to role message
                for i in range(12):
                    await role_message.add_reaction(
                        emojize(emoji_dict_keys[i]))

                # add reactions to registration message
                for i in range(15, 17):
                    await role_message.add_reaction(
                        emojize(emoji_dict_keys[i]))

                # save ids to dictionary to be save in json file
                reg_data['reg_message_id'] = reg_message.id
                reg_data['role_message_id'] = role_message.id

                # save data to dictionary and json file
                j_data['reg_data'] = reg_data
                json.dump(j_data, 'config_test.json')
                pass

            self.role_channel_id = reg_data['role_channel_id']
            self.role_message_id = reg_data['role_message_id']
        pass

    # get message string from json file
    def get_message_from_json(data: str) -> str:
        messages: dict = json.load(open('messages.json'))
        return messages[data]
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,
                                  payload: discord.RawReactionActionEvent):
        '''
        Only does something when users react to a specific message
        Gives user role depending on reaction only if they are
        registered/students
        '''
        # ignore everything is user is bot
        if payload.user_id == self.bot.user.id:
            return

        emoji: str = demojize(payload.emoji.name)
        if emoji not in self.role_dict:
            return
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)

        member: discord.Member = guild.get_member(payload.user_id)
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)

        # will throw an error if the emoji doesn't exist in the dictionary
        role: discord.Role = guild.get_role(self.role_dict[emoji])

        # handles reactions to reg message
        if payload.message_id == self.reg_message_id:
            # the user wants to get student tag
            if emoji == ":graduation_cap:":
                self.register(channel, member, role, emoji)
                pass
            # the user wants to get guest tag
            if emoji == ":spy:":
                await self.add_guest(channel, member)
                pass
            pass

        if payload.message_id == self.role_message_id:
            await self.give_role(channel, member, role)
            pass
        pass

    async def register(self, channel: discord.TextChannel,
                       member: discord.Member, emoji: str) -> bool:
        """
        Checks if the user is registered.
        If they are give them student role and send affirmative message,
        else send them negative message.
        """
        if sql_handler.is_registered(member.name, member.user.discriminator):
            await member.add_roles(self.bot.get_role(
                self.role_dict[':graduation_cap:']))  # give role
            # send a confirmation message
            await channel.send(content=self.get_message_from_json(
                "reg_suc_message").format(member.mention), delete_after=3)
            pass
        else:
            # send a negative message
            await channel.send(content=self.get_message_from_json(
                "not_reg_message").format(member.mention), delete_after=3)
            channel.fetch_message(self.reg_message_id).remove_reaction(
                emojize(emoji), member)  # remove user reaction from message
        pass

    async def add_geust(self, channel: discord.TextChannel,
                        member: discord.Member):
        await member.add_roles(self.bot.get_tole(
            self.role_dict[':detective:']))  # give guest role
        await channel.send(content=self.get_message_from_json(
            "guest_message").format(member.mention), delete_after=3)
        pass

    async def give_role(self, channel: discord.TextChannel,
                        member: discord.Member, role: discord.Role):
        """
        Gives the member a role/tag.
        First it checks if the member is register,
        have the mcmaster student tag.
        """
        if "mcmaster student" not in [role.name.lower
                                      for role in member.roles]:
            await channel.send(content=self.get_messge_from_json("role_fail"),
                               delete_after=3)
            pass
        else:
            if role not in [role for role in member.role]:
                await member.add_roles(role)
                await channel.send(content=self.get_message_from_json(
                    "role_suc").format(member.mention), delete_after=3)
                pass
            else:
                await channel.send(content=self.get_message_from_json(
                    "role_exit"), delte_after=3)
                pass
        pass
    pass

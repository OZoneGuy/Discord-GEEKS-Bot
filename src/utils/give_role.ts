import { CommandInteraction, GuildManager, GuildMemberManager, MessageReaction, PartialMessageReaction, PartialUser, RoleManager, User } from "discord.js";
import { add_reaction, get_guest_role, get_member_role, get_message_id } from "./database/db";
import { logger } from "./logger";

export async function give_role_command(
    guild_id: string,
    role_function: (guild_id: string) => Promise<string | null | undefined>,
    interaction: CommandInteraction): Promise<void> {

    const role_id = await role_function(guild_id)
    switch (role_id) {
        case null:
            interaction.reply("Couldn't find the server. Maybe it is not registered")
            break;
        case undefined:
            interaction.reply("The admins didn't register a guest role yet.")
            break;
        default:
            const guildManager = new GuildManager(interaction.client)
            const guild = await guildManager.fetch(guild_id)

            const roleManager = new RoleManager(guild)
            const role = await roleManager.fetch(role_id)
            if (role) {
                const memberManager = new GuildMemberManager(guild)
                const member = await memberManager.fetch(interaction.user)
                if (member.roles.cache.has(role.id)) {
                    interaction.reply(`You already have the **${role.name}** role in **${guild.name}**`)
                } else {
                    member.roles.add(role)
                    interaction.reply(`Gave you the **${role.name}** in **${guild.name}**, enjoy your stay!`)
                }
            } else {
                interaction.reply("Couldn't find the role. Please contact the admins.")
            }
            break;
    }

}

export async function give_role_message(
    msg_reaction: MessageReaction | PartialMessageReaction,
    user: User | PartialUser): Promise<void> {

    const guild = msg_reaction.message.guild
    if (guild) {
        const reg_msg_id = await get_message_id(guild.id)
        if (reg_msg_id === msg_reaction.message.id) {
            const reaction_result = await add_reaction(user.id)
            var role_id: string | null | undefined;
            switch (reaction_result) {
                case undefined: // Haven't attempted to register
                    user.send("You still need to verify email or register as a guest.")
                    return;
                case null: // Failed to save
                    user.send("Failed to register your reaction, please remove your reaction and try again.")
                    return;
                case true: // A member
                    role_id = await get_member_role(guild.id)
                    break;
                case false: // A guest
                    role_id = await get_guest_role(guild.id)
                    break;
            }

            switch (role_id) {
                case null:
                    user.send(`The admins didn't register the ${guild.name} server, please contact them.`)
                    break;
                case undefined:
                    user.send("The didn't setup a guest role, please contact them.")
                    break;
                default:
                    const role_manager = new RoleManager(guild)
                    const role = await role_manager.fetch(role_id)
                    if (role) {
                        const memManager = new GuildMemberManager(guild)
                        const member = await memManager.fetch(user.id)
                        if (member.roles.cache.has(role.id)) {
                            member.send(`You already have the **${role.name}** role in **${guild.name}**`)
                        } else {
                            member.roles.add(role)
                            member.send(`Gave you the **${role.name}** in **${guild.name}**`)
                        }
                    } else {
                        logger.error(`Couldn't find ${role_id} role in ${guild.name} for message ${msg_reaction.message.id}`)
                    }
                    break;
            }
        }
    }
}

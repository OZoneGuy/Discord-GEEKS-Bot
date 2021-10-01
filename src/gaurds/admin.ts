import { CommandInteraction, GuildMember, Permissions } from "discord.js";
import { GuardFunction } from "discordx";

export const isAdmin : GuardFunction<CommandInteraction> =
    async (interaction, _client, next): Promise<void> => {
        const mem = interaction.member;

        // I don't think I like this way of doing things... But I am trying it :/
        mem instanceof GuildMember &&
            mem.permissions.has(Permissions.FLAGS.ADMINISTRATOR) &&
            await next();
    }

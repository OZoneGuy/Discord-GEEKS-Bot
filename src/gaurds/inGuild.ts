import { CommandInteraction } from "discord.js";
import { GuardFunction } from "discordx";

export const inGuild: GuardFunction<CommandInteraction> =
    async (interaction, _client, next) => {
        if (interaction.inGuild()){
            await next()
        } else {
            interaction.reply("Please use this command from the server you want to register")
        }
    }

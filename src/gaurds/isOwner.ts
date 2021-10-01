import { CommandInteraction } from "discord.js";
import { GuardFunction } from "discordx";
import { owner_id } from '../../config/secret_config.json'

export const isOwner: GuardFunction<CommandInteraction> =
    async (interaction, _client, next) => {
        interaction.user.id == owner_id && await next()
    }

import { CommandInteraction, Guild, Permissions } from "discord.js";
import { Discord, Guard, Slash } from "discordx";
import { isAdmin } from "../gaurds/admin";
import { inGuild } from "../gaurds/inGuild";
import { add_guild } from '../utils/database/db'

@Discord()
@Guard(isAdmin, inGuild)
abstract class AppDiscord {
    @Slash("register_server")
    private register_server(interaction: CommandInteraction): void {

        const guild: Guild = interaction.guild!
        add_guild(guild.id, guild.name).then((res) => {
            if (res) {
                interaction.reply(`Successfully added ${guild.name} to the database!`)
            } else {
                interaction.reply(`Failed to add ${guild.name} to the database!`)
            }
        })
    }
}

import { CommandInteraction } from "discord.js";
import { Discord, Slash, SlashOption } from "discordx";
import { get_guest_role, reg_guest } from "../utils/database/db";
import { give_role_command } from "../utils/give_role";
// import {get_member_role}

@Discord()
abstract class AddDiscord {

    @Slash("guest")
    guest(
        @SlashOption("server_id", { required: false, type: "STRING" })
        i_guild_id: string | undefined,

        interaction: CommandInteraction) {

        const guild_id = interaction.guild?.id || i_guild_id

        if (guild_id) {
            reg_guest(interaction.user.id)
                .then((res) => {
                    switch (res) {
                        case true: // Agreed to the rules
                            give_role_command(guild_id, get_guest_role, interaction)
                            break;
                        case false:
                            interaction.reply("You still need to accept the rules")
                            break;
                        case null:
                            interaction.reply("Failed to register for guest role. Please try again or contact the admins.")
                            break
                    }
                })
        } else {
            interaction.reply("You need to call this from a server or provide the server id.")
        }
    }
}

import { CommandInteraction } from "discord.js";
import { Discord, Guard, Slash, SlashOption } from "discordx";
import { isAdmin } from "../gaurds/admin";
import { set_message_id } from "../utils/database/db";

@Discord()
abstract class AppDiscord {
    @Guard(isAdmin)
    @Slash("set_registration_messatge")
    set_reg_email(@SlashOption("message_id", {required: true, description: "The id of the message to listen to"})
                  message_id: string,
                  @SlashOption("server_id", {required: false, type: "STRING", description: "The id of the server."})
                  guild_id: string | undefined,
                  interaction: CommandInteraction) {
        guild_id = interaction.guild?.id || guild_id
        if (guild_id) {
            set_message_id(guild_id, message_id)
                .then((res) => {
                    if (res) {
                        interaction.reply("Saved message id")
                    } else if (res === null) {
                        interaction.reply("Unable to find the guild")
                    } else {
                        interaction.reply("Unable to save the message id")
                    }
                })
        } else {
            interaction.reply("Please specify the server id or call this from a server")
        }
    }
}

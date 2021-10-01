import { CommandInteraction } from "discord.js";
import { Discord, Guard, Slash, SlashOption } from "discordx";
import { isAdmin } from "../gaurds/admin";
import { set_email_tail } from "../utils/database/db";

@Discord()
abstract class AppDiscord {

    @Guard(isAdmin)
    @Slash("set_email")
    set_email(
        @SlashOption("email_tail", { required: true })
        email_tail: string,
        @SlashOption("server_id", {
            required: false,
            type: "STRING"
        })
        guild_id: string | undefined,
        interaction: CommandInteraction) {
        guild_id = interaction.guild?.id || guild_id

        if (guild_id) {
            set_email_tail(guild_id, email_tail)
                .then((res) => {
                    if (res) {
                        interaction.reply("Registered email tail successfully")
                    } else if (res === null) {
                        interaction.reply("Couldn't find your server")
                    } else {
                        interaction.reply("Failed to add the email tail, not sure why.")
                    }
                })
        } else {
            interaction.reply("Please specify a server id or call this from a server")
        }
    }
}

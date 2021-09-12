import { CommandInteraction } from "discord.js";
import { Discord, Slash, SlashOption } from "discordx";
import { get_email_tail, get_member_role, reg_email } from "../utils/database/db";
import { give_role_command } from "../utils/give_role";

@Discord()
abstract class AppDiscord {

    @Slash("register_email")
    register_email(
        @SlashOption("email", {
            required: true,
            description: "The email to register with"
        })
        email: string,
        @SlashOption("server", {
            required: false,
            description: "The id of the server you want to register in",
            type: "STRING"
        })
        i_guild_id: string | undefined,
        interaction: CommandInteraction) {

        // make sure the guild is specified
        const guild_id = interaction.guild?.id || i_guild_id
        if (!guild_id) {
            interaction.reply("You need to specify a server id or call this command from the server")
            return
        }

        get_email_tail(guild_id)
            .then((email_tail) => {
                if (!email_tail)
                    interaction.reply("The server admins did not register the server, please contact them for further details.");
                else {
                    const email_tester: RegExp = new RegExp(`^.*@${email_tail}`);
                    if (email_tester.test(email)) {
                        reg_email(interaction.user.id)
                            .then((res) => {
                                switch (res) {
                                    case true: // Agreed to the rules
                                        give_role_command(guild_id, get_member_role, interaction)
                                        break;
                                    case false:
                                        interaction.reply("You still need to accept the rules")
                                        break;
                                    case null:
                                        interaction.reply("Failed to register for guest role. Please try again or contact the admins.")
                                        break
                                }
                            })
                    }
                    else
                        interaction.reply("Failed to register, could not match email address.");
                }
            })
    }
}

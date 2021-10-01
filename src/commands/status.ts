import { CommandInteraction } from "discord.js";
import { Discord, Slash } from "discordx";

@Discord()
abstract class AppDiscord {

    @Slash("status")
    status(interaction: CommandInteraction) {
        interaction.reply("I am doing fine, thanks for asking.")
    }
}

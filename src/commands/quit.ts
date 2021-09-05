import { CommandInteraction } from "discord.js";
import { Discord, Guard, Slash } from "discordx";
import { isOwner } from "../gaurds/isOwner";
import { close_db_connections } from "../utils/database/db";
import { logger } from "../utils/logger";

@Discord()
@Guard(isOwner)
abstract class AddDiscord {

    @Slash("quit")
    private quit(interaction: CommandInteraction): void {
        logger.info("Starting termination process..")
        close_db_connections()
        logger.info("Logging client off...")
        interaction.client.destroy()
        logger.info("Logged client off")
    }
}

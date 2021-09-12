import { MessageReaction, PartialMessageReaction, PartialUser, User } from "discord.js";
import { Discord, On } from "discordx";
import { give_role_message } from "../utils/give_role";

@Discord()
abstract class AppDiscord {

    @On("messageReactionAdd")
    add_reaction(
        message: MessageReaction | PartialMessageReaction,
        user: User | PartialUser) {
        give_role_message(message, user)
    }
}

import { Client } from "discord.js";
import { ArgsOf, Discord, On } from "discordx";
import { give_role_message } from "../utils/give_role";

@Discord()
abstract class AppDiscord {

    @On("messageReactionAdd")
    add_reaction(
        [reaction_msg, user]: ArgsOf<"messageReactionAdd">,
        _client: Client,
        _guardPayload: any) {
        give_role_message(reaction_msg, user)
    }
}

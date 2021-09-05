import { CommandInteraction, Role } from "discord.js";
import { Discord, Guard, Slash, SlashOption } from "discordx";
import { isAdmin } from "../gaurds/admin";
import { set_member_role } from "../utils/database/db";

@Discord()
@Guard(isAdmin)
abstract class AddDiscord {
    @Slash("set_members_role")
    private set_members_role(@SlashOption("Role", { required: true }) role: Role,
                             interaction: CommandInteraction) {
        const guild_id = interaction.guild!.id
        set_member_role(guild_id, role.id).then((res) => {
            switch (typeof res) {
                case "boolean":
                    if (res) {
                        interaction.reply(`Successfully set the member's role to ${Role.name}`)
                    } else {
                        interaction.reply(`Failed to set the member's role`)
                    }
                    break;
                default:
                    interaction.reply(`Could not find the guild, make sure that you used \`/register_server\``)
                    break;
            }
        })
    }
}

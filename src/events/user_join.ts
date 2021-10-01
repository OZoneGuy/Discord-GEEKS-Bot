import { GuildMember } from "discord.js";
import { Discord, On } from "discordx";

@Discord()
abstract class AppDiscord {


    @On("guildMemberAdd")
    member_join(member: GuildMember) {
        member.send(`Hello ${member.user.username}, and welcome to ${member.guild.name}!
If you would like access to the server you need to accept the rules then register with me.
To do so, you need to use either the \`register_email\` command or \`guest\` command.`)
    }
}

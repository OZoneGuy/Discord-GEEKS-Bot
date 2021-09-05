import { connect, connection, model, Schema } from "mongoose";
import { logger } from '../logger';

const host: string = process.env["MON_HOST"] || "127.0.0.1";
const port: string = process.env["MON_PORT"] || "0000";
const db: string = process.env["MON_DATABASE"] || "bot";

const username: string = process.env["MON_USERNAME"] || "kevin";
const password: string = process.env["MON_PASSWORD"] || "hart";

export interface GuildInfo {
    guildId: string,
    guildName: string,
    member_role?: string,
    guest_role?: number,
    email_tail?: string,
    message_id?: number
}

const guild_schema = new Schema<GuildInfo>({
    guildId: { type: String, required: true },
    guildName: { type: String, required: true },
    member_role: String,
    guest_role: Number,
    email_tail: String,
    message_id: Number
})

const GuildModel = model<GuildInfo>('GuildInfo', guild_schema)

/**
 * Connects to the MongoDB database
 */
export async function connect_to_db(): Promise<null | typeof import("mongoose")>{
    return connect(`mongodb://${host}:${port}`,
        { user: username, pass: password, dbName: db })
        .catch((err) => {
            logger.error(`Failed to connect to ${db} at ${host}:${port}`)
            logger.error(`Received error: ${err}`)
            return null
        })
}

/**
 * Closes Database Connection
 */
export async function close_db_connections() {
    logger.info("Closing MongoDB connection...")
    connection.close().then(() => {
        logger.info("Closed MongoDB connection.")
    }).catch((err) => {
        logger.error(`Failed to close MongoDB connection with error: ${err}`)
    })
}

/**
 * @description Add a guild to the database
 *
 * @param id: guild id to be added
 * @param name: guild id to be added
 *
 * @returns Promise<true> if it was successful, and Promise<false> otherwise
 */
export async function add_guild(id: string, name: string): Promise<boolean> {
    const new_guild = new GuildModel({
        guildId: id,
        guildName: name.toLowerCase()
    });

    return new_guild.save()
        .then((_) => {
            logger.info(`Successfully added ${name} with ${id} id`)
            return true
        })
        .catch((_) => {
            logger.error(`Failed to add guild - id: ${id}, name: ${name}`)
            return false
        });
}

/**
 * @description Set the member role for the given guild
 *
 * @param guild_id: the id of the guild to update
 * @param role: the id of the role to set as the members role
 *
 * @returns true if successful, false if not successful, and null if it was unable to find the guild object
 */
export async function set_member_role(guild_id: string, role: string): Promise<boolean | null> {

    let result = await GuildModel.findOneAndUpdate({ guildId: guild_id }, { member_role: role },
                                                   {new: true}).exec();
    if (result) {
        if (result.member_role == role) {
            logger.info(`Successfully set member role (${role}) for guild ${result.guildName}`)
            return true
        } else {
            logger.error(`Failed to set member role to ${role} for ${result.guildName}`)
            return false
        }
    } else {
        logger.error(`Couldn't find guild with id ${guild_id}`)
        return null
    }

}

/**
 * @description Retrieves the members role for the given guild
 *
 * @param guild_id: The id of the guild to get the members role for
 *
 * @returns null if it could not find the guild object, undefined if `member_role` is not defined, and the `member_role` if it is defined
 */
export async function get_member_role(guild_id: string): Promise<string | null | undefined>{
    let result = await GuildModel.findOne({guildId: guild_id}).exec();
    return result && result.member_role
}

/**
 * @description Set the guest role for the given guild
 *
 * @param guild_id: the id of the guild to update
 * @param role: the id of the role to set as the guests role
 *
 * @returns true if successful, false if not successful, and null if it was unable to find the guild object
 */
export async function set_guest_role(guild_id: string, role: number): Promise<boolean | null> {

    let result = await GuildModel.findOneAndUpdate({ guildId: guild_id }, { guest_role: role }).exec();

    if (result) {
        if (result.guest_role == role) {
            logger.info(`Successfully set guest role (${role}) for guild ${result.guildName}`)
            return true
        } else {
            logger.error(`Failed to set guest role to ${role} for ${result.guildName}`)
            return false
        }
    } else {
        logger.error(`Couldn't find guild with id ${guild_id}`)
        return null
    }
}

/**
 * @description Retrieves the guests role for the given guild
 *
 * @param guild_id: The id of the guild to get the guests role for
 *
 * @returns null if it could not find the guild object, undefined if `guest_role` is not defined, and the `guest_role` if it is defined
 */
export async function get_guest_role(guild_id: string): Promise<number | undefined | null> {
    let result = await GuildModel.findOne({ guildId: guild_id }).exec();
    return result && result.guest_role
}

/**
 * @description set the email tail for the given guild
 *
 * @param guild_id: the id of the guild to update
 * @param email_tag: the email tail
 *
 * @returns true if successful, false if not successful, and null if it was unable to find the guild object
 */
export async function set_email_tail(guild_id: string, email_tail: string): Promise<boolean | null> {

    let result = await GuildModel.findOneAndUpdate({guildId: guild_id}, {email_tail: email_tail});

    if (result) {
        if (result.email_tail == email_tail) {
            logger.info(`Successfully set email (${email_tail}) for guild ${result.guildName}`)
            return true
        } else {
            logger.error(`Failed to set email to ${email_tail} for ${result.guildName}`)
            return false
        }
    } else {
        logger.error(`Couldn't find guild with id ${guild_id}`)
        return null
    }
}

/**
 * @description Retrieves the members role for the given guild
 *
 * @param guild_id: The id of the guild to get the members role for
 *
 * @returns null if it could not find the guild object, undefined if `email_tail` is not defined, and the `email_tail` if it is defined
 */
export async function get_email_tail(guild_id: string): Promise<string | undefined | null> {
    let result = await GuildModel.findOne({guildId: guild_id}).exec();
    return result && result.email_tail
}

/**
 * @description set the message id for registration reactions for the given guild
 *
 * @param guild_id: the id of the guild to update
 * @param message_id: the message id
 *
 * @returns true if successful, false if not successful, and null if it was unable to find the guild object
 */
export async function set_message_id(guild_id: string, message_id: number): Promise<boolean | null> {
    let result = await GuildModel.findOneAndUpdate({guildId: guild_id, message_id: message_id});

    if (result) {
        if(result.message_id == message_id) {
            logger.info(`Successfully set message (${message_id}) for guild ${result.guildName}`)
            return true
        } else {
            logger.error(`Failed to set message to ${message_id} for ${result.guildName}`)
            return false
        }
    } else {
        logger.error(`Couldn't find guild with id ${guild_id}`)
        return null
    }
}

/**
 * @description Retrieves the members role for the given guild
 *
 * @param guild_id: The id of the guild to get the members role for
 *
 * @returns null if it could not find the guild object, undefined if `message_id` is not defined, and the `message_id` if it is defined
 */
export async function get_message_id(guild_id: string): Promise<number | undefined | null> {
    let result = await GuildModel.findOne({ guildId: guild_id }).exec();
    return result && result.message_id
}

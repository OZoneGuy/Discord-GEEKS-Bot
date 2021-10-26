import { connect, connection, model, Schema } from "mongoose";
import { logger } from '../logger';

const host: string = process.env["MON_HOST"] || "127.0.0.1";
const port: string = process.env["MON_PORT"] || "0000";
const db: string = process.env["MON_DATABASE"] || "bot";

const username: string = process.env["MON_USERNAME"] || "kevin";
const password: string = process.env["MON_PASSWORD"] || "hart";

export interface GuildInfo {
    _id: string,
    guildName: string,
    member_role?: string,
    guest_role?: string,
    email_tail?: string,
    message_id?: string
}
export interface MemberInfo {
    _id: string,
    email_ver?: boolean,
    reaction: boolean
}

const guild_schema = new Schema<GuildInfo>({
    _id: { type: String, alias: 'guildId' },
    guildName: { type: String, required: true },
    member_role: String,
    guest_role: String,
    email_tail: String,
    message_id: String
})

const member_schema = new Schema<MemberInfo>({
    _id: { type: String, alias: 'userId' },
    email_ver: { type: Boolean, default: undefined },
    reaction: { type: Boolean, required: true }
})

const GuildModel = model<GuildInfo>('GuildInfo', guild_schema)
const MemberModel = model<MemberInfo>('MemberInfo', member_schema)

/**
 * Connects to the MongoDB database
 */
export async function connect_to_db(): Promise<null | typeof import("mongoose")> {
    return connect(`mongodb://${username}:${password}@${host}:${port}`)
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

    let doc = await GuildModel.findById(guild_id).exec();


    if (doc) {
        doc.member_role = role
        return doc.save().then((new_doc) => {
            if (new_doc.member_role == role) {
                logger.info(`Successfully set member role (${role}) for guild ${new_doc.guildName}`)
                return true
            } else {
                logger.error(`Failed to set member role to ${role} for ${new_doc.guildName}`)
                return false
            }
        })
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
export async function get_member_role(guild_id: string): Promise<string | null | undefined> {
    let result = await GuildModel.findById(guild_id).exec();
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
export async function set_guest_role(guild_id: string, role: string): Promise<boolean | null> {

    let doc = await GuildModel.findById(guild_id).exec();

    if (doc) {
        doc.guest_role = role
        return doc.save().then((new_doc) => {
            if (new_doc.guest_role == role) {
                logger.info(`Successfully set guest role (${role}) for guild ${new_doc.guildName}`)
                return true
            } else {
                logger.error(`Failed to set guest role to ${role} for ${new_doc.guildName}`)
                return false
            }
        })
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
export async function get_guest_role(guild_id: string): Promise<string | undefined | null> {
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

    email_tail = email_tail.replace('.', '\.')
    let doc = await GuildModel.findById(guild_id).exec();

    if (doc) {
        doc.email_tail = email_tail
        return doc.save().then((new_doc) => {
            if (new_doc.email_tail == email_tail) {
                logger.info(`Successfully set email (${email_tail}) for guild ${new_doc.guildName}`)
                return true
            } else {
                logger.error(`Failed to set email to ${email_tail} for ${new_doc.guildName}`)
                return false
            }
        })
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
    let result = await GuildModel.findById(guild_id).exec();
    return result && result.email_tail
}

/**
 * @description set the message id for registration reactions for the given guild
 *
 * @param guild_id: the id of the guild to update
 * @param message_id: the message id
 *
 * @returns `true` if successful, `false` if not successful, and `null` if it was unable to find the guild object
 */
export async function set_message_id(guild_id: string, message_id: string): Promise<boolean | null> {
    let doc = await GuildModel.findById(guild_id).exec();

    if (doc) {
        doc.message_id = message_id
        return doc.save().then((new_doc) => {
            if (new_doc.message_id == message_id) {
                logger.info(`Successfully set message (${message_id}) for guild ${new_doc.guildName}`)
                return true
            } else {
                logger.error(`Failed to set message to ${message_id} for ${new_doc.guildName}`)
                return false
            }
        })
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
export async function get_message_id(guild_id: string): Promise<string | undefined | null> {
    let result = await GuildModel.findById(guild_id).exec();
    return result && result.message_id
}

/**
 * @description Records that the user reacted to the rules message. Sets
 *
 * @param user_id: The id of the user who reacted to the message
 *
 * @return null if failed to save the reaction, `true` if they registered their email, `false` otherwise, and `undefined` if they haven't requested anything yet
 */
export async function add_reaction(user_id: string): Promise<boolean | null | undefined> {
    let result = await MemberModel.findById(user_id).exec()

    if (result) {
        result.reaction = true
        return result.save()
            .then((new_mem) => {
                if (new_mem.reaction)
                    return new_mem.email_ver
                else {
                    logger.error(`Failed update reaction for ${user_id}`)
                    return null
                }
            })
            .catch((err) => {
                logger.error(`Failed to register user reaction: ${err}`)
                return null
            })
    } else {
        const new_member = new MemberModel({
            _id: user_id,
            reaction: true
        })

        return new_member.save()
            .then((res) => { return res.email_ver})
            .catch((err) => {
                logger.error(`Failed to register user reaction: ${err}`)
                return null
            })
    }
}

/**
 * @description Record that an email has been registered for the given user
 *
 * @param user_id: The id of the user who registered their email
 *
 * @return Null if it failed to record email, false if the user didn't give reaction, and true if the user reacted
 */
export async function reg_email(user_id: string): Promise<boolean | null> {
    const user = await MemberModel.findById(user_id).exec();

    if (user) {
        user.email_ver = true
        return user.save()
            .then((new_doc) => {
                logger.debug(`Updated ${new_doc}`)
                switch (new_doc.email_ver) {
                    case true:
                    case false:
                        return user.reaction
                    case undefined:
                        logger.debug(`email_ver: ${new_doc.email_ver}`)
                        logger.error(`Failed to register as guest for ${user_id}`)
                        return null
                }
            })
            .catch((err) => {
                logger.error(`Error when recording registered email for ${user_id}: ${err}`)
                return null
            })
    } else {
        const new_member = new MemberModel({
            userId: user_id,
            email_ver: true,
            reaction: false
        })

        return new_member.save()
            .then((_) => { return false })
            .catch((err) => {
                logger.error(`Failed to register user email: ${err}`)
                return null
            })
    }
}

/**
 * @description Record that no email has been registered for the given user
 *
 * @param user_id: The id of the user who didn't register their email
 *
 * @return Null if it failed to record email, false if the user didn't give reaction, and true if the user reacted
 */
export async function reg_guest(user_id: string): Promise<boolean | null> {

    const user = await MemberModel.findById(user_id).exec();

    if (user) {
        user.email_ver = false
        return user.save()
            .then((new_doc) => {
                switch (new_doc.email_ver) {
                    case true:
                    case false:
                        return user.reaction
                    case undefined:
                        logger.error(`Failed to register as guest for ${user_id}`)
                        return null
                }
            })
            .catch((err) => {
                logger.error(`Error when registering as guest for ${user_id}: ${err}`)
                return null
            })
    } else {
        const new_member = new MemberModel({
            userId: user_id,
            email_ver: false,
            reaction: false
        })

        return new_member.save()
            .then((_) => { return false })
            .catch((err) => {
                logger.error(`Failed to register as guest for ${user_id}: ${err}`)
                return null
            })
    }
}

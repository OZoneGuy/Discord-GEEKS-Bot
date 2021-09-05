import "reflect-metadata";
import { Client } from "discordx";
import { Intents } from "discord.js";

import { test_token as token } from "../config/secret_config.json";
import { connect_to_db } from "./utils/database/db";

async function start() {
    const client: Client = new Client({
        intents: [
            Intents.FLAGS.GUILDS,
            Intents.FLAGS.DIRECT_MESSAGES,
            Intents.FLAGS.GUILD_MESSAGES,
            Intents.FLAGS.DIRECT_MESSAGE_REACTIONS
        ],
        requiredByDefault: true,
        classes: [
            `${__dirname}/events/*.{ts,js}`,
            `${__dirname}/commands/*.{ts,js}`,
            `${__dirname}/guards/*.{ts,js}`,
        ]
    });

    client.once("ready", async () => {
        await client.initApplicationCommands();
        console.log("Bot is logged in!");
    });

    client.on("interactionCreate", (interaction) => {
        client.executeInteraction(interaction);
    });

    const db_conn = await connect_to_db()
    if (!db_conn)
        return;
    await client.login(token);
}

start();

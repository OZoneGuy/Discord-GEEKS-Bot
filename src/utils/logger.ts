import { config, createLogger, format, transports } from "winston";

export const logger = createLogger({
    levels: config.syslog.levels,
    format: format.json(),
    transports: [
        new transports.Console({level: 'warn'}),
        new transports.File({filename: 'logs/combined.log', level: 'info'}),
        new transports.File({filename: 'logs/errors.log', level: 'error'})
    ]
})

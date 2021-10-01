import { config, createLogger, format, transports } from "winston";


export const logger = createLogger({
    levels: config.cli.levels,
    format: format.combine(format.timestamp(),
                           format.prettyPrint()),
    transports: [
        new transports.Console({level: 'warn',
                                format: format.combine(format.timestamp(),
                                                       format.cli())}),
        new transports.File({filename: 'logs/combined.log',
                             level: 'info'}),
        new transports.File({filename: 'logs/errors.log',
                             level: 'error'})
    ],
})

#!/usr/bin/env python3

import argparse
import telegram.ext as te
import warbot
import logging
import storage


def create_parser():
    desc = ''
    ep = ''

    parser = argparse.ArgumentParser(description=desc, epilog=ep)
    parser.add_argument('--token', dest='token', required=True)
    parser.add_argument('--host', dest='host', required=True)
    parser.add_argument('--dbuser', dest='dbuser', required=True)
    parser.add_argument('--dbpasswd', dest='dbpasswd', required=True)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # bot auth
    updater = te.Updater(token=args.token)
    dispatcher = updater.dispatcher

    st = storage.Storage(args.host, args.dbuser, args.dbpasswd)
    war_bot = warbot.WarBot(storage=st)

    # TODO better logging!
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info('bot from project "ne0wargame_bot" has started...')

    help_handler = te.CommandHandler('help', war_bot.send_help)
    dispatcher.add_handler(help_handler)

    stats_handler = te.CommandHandler('stats', war_bot.send_stats)
    dispatcher.add_handler(stats_handler)

    statsv_handler = te.CommandHandler('statsv', war_bot.send_statsv)
    dispatcher.add_handler(statsv_handler)

    end_handler = te.CommandHandler('end', war_bot.end_wargame)
    dispatcher.add_handler(end_handler)

    msg_handler = te.MessageHandler(te.Filters.text, war_bot.analyze_msg)
    dispatcher.add_handler(msg_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()

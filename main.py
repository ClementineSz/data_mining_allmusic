import argparse
import logging
import sys

from nicelog.formatters import Colorful

from database import database_manager
from orchestration import orchester

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(Colorful())
logger.addHandler(handler)


def main():
    my_parser = argparse.ArgumentParser()

    # Add the arguments
    my_parser.add_argument('task',
                           help="Input the name of the task: create_database, create_tables, drop_tables, drop_database, scrape")
    my_parser.add_argument('-m', '--mood', type=str, help='Print good morning')

    args = my_parser.parse_args()

    if args.task == 'create_database':
        database_manager.create_database()
    if args.task == 'refresh_tables':
        database_manager.refresh_tables()
    elif args.task == 'create_tables':
        database_manager.create_tables()
    elif args.task == 'drop_tables':
        database_manager.drop_tables()
    elif args.task == 'drop_database':
        database_manager.drop_database()
    elif args.task == 'scrape':
        orchester.orchestrate(args.mood)


if __name__ == '__main__':
    main()

import argparse

from database import database_manager
from scraping.scraper import get_new_albums


def main():
    my_parser = argparse.ArgumentParser()

    # Add the arguments
    my_parser.add_argument('task',
                           help="Input the name of the task: create_database, create_tables, drop_tables, drop_database, scrape")
    my_parser.add_argument('-m', '--mood', type=str, help='Print good morning')

    args = my_parser.parse_args()

    if args.task == 'create_database':
        database_manager.create_database()
    elif args.task == 'create_tables':
        database_manager.create_tables()
    elif args.task == 'drop_tables':
        database_manager.drop_tables()
    elif args.task == 'drop_database':
        database_manager.drop_database()
    elif args.task == 'scrape':
        albums = get_new_albums()
        if args.mood:
            albums = [album for album in albums if args.mood.title() in album.details.moods]
        database_manager.insert_albums(albums)


if __name__ == '__main__':
    main()

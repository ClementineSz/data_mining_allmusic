from database import database_manager
from scraping.scraper import get_new_albums

def main():
    albums = get_new_albums()
    database_manager.insert_albums(albums)


if __name__ == '__main__':
    main()

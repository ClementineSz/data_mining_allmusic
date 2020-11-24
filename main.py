from database import database_manager
from scraping.allmusic_scraper import get_new_albums

def main():
    albums = get_new_albums()
    database_manager.insert(albums)


if __name__ == '__main__':
    main()

from scraping.allmusic_scraper import get_new_albums


def main():
    albums = get_new_albums()
    for album in albums:
        for i in album.details.reviews:
            print(i.name)


if __name__ == '__main__':
    main()

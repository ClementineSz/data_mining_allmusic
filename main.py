from allmusic_scraper import get_new_albums


def main():
    albums = get_new_albums()
    for album in albums:
        print(album.details.duration)


if __name__ == '__main__':
    main()

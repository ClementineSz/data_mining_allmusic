import requests
from bs4 import BeautifulSoup

from album import Album

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"

NEW_RELEASES = 'https://www.allmusic.com/newreleases'


def get_new_releases():
    """

    :return: [{
        artist_name: 'Bruce Springsteen',
        album_name: 'Letter to You'
    },
    ]
    """
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(NEW_RELEASES, headers=headers)
    html = response.text
    with open('allmusic.html', 'w') as f:
        f.write(html)
    soup = BeautifulSoup(html, 'html.parser')

    # Extract all new features from the html
    albums_divs = soup.find_all('div', {"class": "new-release"})

    # Create dictionary of data : artist, name of album and genre
    new_features = {}
    new_features_list = []

    albums = [Album(album_div) for album_div in albums_divs]
    for album in albums:
        print(album.url)
    # for div in albums_divs:
        # album = Album(div)
        # albums.append(album)



        # new_features['artist'] = div.find('div', {"class": "artist"}).text.strip()
        # new_features['album'] = div.find('div', {"class": "title"}).text.strip()
        # new_features['genres'] = div.find('div', {"class": "genres"}).text.strip()
        # new_features['label'] = div.find('div', {"class": "labels"}).text.strip()
        # new_features['label'] = div.find('div', {"class": "allmusic-rating-new"}).text.strip()
        # new_features_list.append(new_features)

    return new_features_list

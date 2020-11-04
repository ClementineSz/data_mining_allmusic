import requests
from bs4 import BeautifulSoup

from models.album import Album
from models.constants import USER_AGENT, BASE_URL, NEW_RELEASES


def get_new_releases():
    """

    :return: [{
        artist_name: 'Bruce Springsteen',
        album_name: 'Letter to You'
    },
    ]
    """
    headers = {"User-Agent": USER_AGENT}
    url = BASE_URL + NEW_RELEASES
    response = requests.get(url, headers=headers)
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
        print(album.details.duration)
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

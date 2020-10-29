import requests
from bs4 import BeautifulSoup

NEW_RELEASES = 'https://www.allmusic.com/newreleases'


def get_new_releases():
    """

    :return: [{
        artist_name: 'Bruce Springsteen',
        album_name: 'Letter to You'
    },
    ]
    """
    response = requests.get(NEW_RELEASES)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    features = {}
    content_dif = soup.find_all('div', {"class" : "meta-container"})

    print(content_dif)

    # for div in content_dif:
    #
    #
    # print(features)

    # TODO

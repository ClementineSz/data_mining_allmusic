import requests
from bs4 import BeautifulSoup

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

    print(html)
    features = {}
    albums_divs = soup.find_all('div', {"class": "new-release"})

    print(albums_divs)

    # for div in content_dif:
    #
    #
    # print(features)

    # TODO

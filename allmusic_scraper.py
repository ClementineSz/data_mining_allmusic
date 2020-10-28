import requests

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
    # TODO

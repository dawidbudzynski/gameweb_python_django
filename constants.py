YEARS = {(x, x) for x in range(1998, 2020)}
SORTED_YEARS = sorted(YEARS, key=lambda x: x[1], reverse=True)

RATING = {(i, '*' * i) for i in range(1, 11)}
SORTED_RATING = sorted(RATING, key=lambda x: x[0], reverse=True)

NEWS_SOURCE_DATA_ALL = {
    'ign': {
        'api_name': 'IGN',
        'image_url': 'img/ign.png'
    },
    'polygon': {
        'api_name': 'Polygon',
        'image_url': 'img/polygon.png'
    },
    'techradar': {
        'api_name': 'TechRadar',
        'image_url': 'img/techradar.png'
    },
    'the-verge': {
        'api_name': 'The Verge',
        'image_url': 'img/verge.png'
    },
}

GAMING_QUOTES = [
    {"quote": "What is better? To be born good or to overcome your evil nature through great effort?",
     "author": "Paarthurnax, Elder Scrolls V: Skyrim"},
    {"quote": "Stand in the ashes of a trillion dead souls, and asks the ghosts if honor matters. "
              "The silence is your answer",
     "author": "Javik, Mass Effect 3"},
    {"quote": "Even in dark times, we cannot relinquish the things that make us human.",
     "author": "Khan, Metro 2033"},
]

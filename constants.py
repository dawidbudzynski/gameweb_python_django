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

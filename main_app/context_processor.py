import csv
import os

from django.conf import settings


def gaming_quotes_processor(request):
    all_quotes = []
    path = os.path.join(settings.MEDIA_ROOT, 'csv/gaming_quotes.csv')
    with open(path) as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            all_quotes.append({'author': row[0], 'quote': row[1]})
    return {'all_quotes': all_quotes}

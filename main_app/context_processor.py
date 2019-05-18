from constants import GAMING_QUOTES


def gaming_quotes_processor(request):
    return {'all_quotes': GAMING_QUOTES}

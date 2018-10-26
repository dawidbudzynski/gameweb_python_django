from constants import GAMING_QUOTES


def gaming_quotes_processor(request):
    all_quotes = GAMING_QUOTES
    return {'all_quotes': all_quotes}

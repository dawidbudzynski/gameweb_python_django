from .models import GamingQuotes


def gaming_quotes_processor(request):
    all_quotes = GamingQuotes.objects.all()
    return {'all_quotes': all_quotes}
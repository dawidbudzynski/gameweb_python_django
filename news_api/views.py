import requests
from decouple import config
from django.shortcuts import render
from django.views import View

from constants import NEWS_SOURCE_DATA_ALL

NEWS_API_KEY = config('NEWS_API_KEY', cast=str)


class TechNewsView(View):
    """Display gaming and tech news using API"""

    def get(self, request, news_source='polygon'):
        image_url = None
        source_name = None
        selected_source = None
        for news_source_key, news_source_values in NEWS_SOURCE_DATA_ALL.items():
            if news_source == news_source_key:
                selected_source = news_source_key
                image_url = news_source_values['image_url']
                source_name = news_source_values['api_name']
        url = (
            'https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(
                selected_source, NEWS_API_KEY)
        )
        response = requests.get(url)
        ctx = {
            'articles': response.json()['articles'],
            'image_url': image_url,
            'source_name': source_name
        }
        return render(
            request,
            template_name='news_main.html',
            context=ctx
        )

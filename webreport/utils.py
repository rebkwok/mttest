import urllib.request
from bs4 import BeautifulSoup


def process_url(url):

    context = {}

    try:
        response = BeautifulSoup(urllib.request.urlopen(url))
    except ValueError:
        context['error'] = "Enter a valid URL"
        return context

    title = response.title.string
    meta = response.meta.prettify()
    context['title'] = title
    context['meta'] = meta

    return context



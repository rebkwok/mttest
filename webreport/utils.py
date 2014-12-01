from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin
import urllib.request
from urllib.error import URLError


from django.template.defaultfilters import filesizeformat

class PageInfo(object):

    def __init__(self, url):
        self.url = url




def process_url(url):

    context = {}

    try:
        response = urllib.request.urlopen(url, timeout=10)
        soup = BeautifulSoup(response)
    except (ValueError, URLError):
        try:
            url = 'http://' + url
            response = urllib.request.urlopen(url, timeout=10)
            soup = BeautifulSoup(response)
        except (ValueError, URLError):
            context['error'] = "Enter a valid URL"
            return context

    html = response.read()

    title = soup.title.string
    meta = soup.findAll("meta")
    meta = str(meta[0])
    meta = meta.split('\n')

    if "Content-Length" in response.headers:
        size = int(response.headers["Content-Length"])
    else:
        size = len(html)

    # remove linebreaks
    text = soup.get_text().rstrip('\n')
    text = text.split()
    unique_words = len(set(text))

    count = Counter(text)
    most_common = count.most_common(5)

    keywords, unused_keywords = keyword_data(soup, text)

    links =  soup.findAll("a", href=True)
    links_result = [(link.string, urljoin(url, link['href'])) for link in links]

    context['url'] = url
    context['title'] = title
    context['meta'] = meta
    context['size'] = filesizeformat(size)
    context['keywords'] = keywords
    context['words'] = len(text)
    context['unique_words'] = unique_words
    context['most_common'] = most_common
    context['unused_keywords'] = unused_keywords
    context['links'] = links_result

    return context

def get_meta_keywords(soup):
  keywords = soup.findAll("meta", attrs={"name":"keywords"})
  if keywords == []:
    return ["No meta keywords"]
  else:
    return keywords[0]['content'].split(',')

def keyword_data(soup, text):
    keywords = get_meta_keywords(soup)
    unused_keywords = []
    if keywords != ["No meta keywords"]:
        for i in keywords:
            if i not in set(text):
                unused_keywords.append(i)

    return keywords, unused_keywords



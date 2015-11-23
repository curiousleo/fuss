from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://ajw.asahi.com'

def _url_from_params(params):
    return '{}/search/?{}'.format(BASE_URL, urlencode(params))

def _url_from_href(href):
    return '{}{}'.format(BASE_URL, href)

def articles(query):
    s = requests.Session()
    page = 1
    found = True

    while found:
        found = False

        url = _url_from_params({'q': query, 'page': page})
        r = s.get(url)
        if r.status_code != 200:
            msg = 'Request to {} failed with status code {}.'.format(url, r.status_code)
            raise Exception(msg)

        soup = BeautifulSoup(r.text, 'html.parser')
        for div in soup.select('.category_box_inner'):
            found = True
            link = div.select('.article_title a')[0]
            article = {
                'url': _url_from_href(link['href']),
                'title': link.get_text(),
                'date': div.select('.article_date')[0].get_text(),
            }
            yield article

        if not found:
            break

        page = page + 1

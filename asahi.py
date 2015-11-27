from time import strptime
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

import fuss
from util import memoize

BASE_URL = 'https://ajw.asahi.com'
DATE_FORMAT = '%B %d, %Y'

class Article(fuss.Article):

    def __init__(self, url, session = None):
        super().__init__(url)

    @property
    def date(self):
        date = self._soup.select('#article .date')[0]
        return strptime(date.get_text(), DATE_FORMAT)

    @property
    def author(self):
        author = self._soup.select('.author')[0]
        return author.get_text()[3:].split('/')[0].title()

    @property
    def title(self):
        return self._soup.select('#article_head h1')[0].get_text()

    @property
    def text(self):
        ps = self._soup.select('.text')[0]
        return ''.join(ps.findAll(text = True)).strip()

fuss.Article.register(Article)

def find(keywords):
    s = requests.Session()
    page = 1
    found = True

    while found:
        found = False

        url = _url_from_params({'q': keywords, 'page': page})
        r = s.get(url)
        if r.status_code != 200:
            msg = 'Request to {} failed with status code {}.'.format(url, r.status_code)
            raise Exception(msg)

        soup = BeautifulSoup(r.text, 'html.parser')
        for div in soup.select('.category_box_inner'):
            found = True
            link = div.select('.article_title a')[0]
            yield _url_from_href(link['href'])

        if not found:
            break

        page = page + 1

def _url_from_params(params):
    return '{}/search/?{}'.format(BASE_URL, urlencode(params))

def _url_from_href(href):
    return '{}{}'.format(BASE_URL, href)

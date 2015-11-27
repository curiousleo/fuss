from time import strptime
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

import fuss
from util import memoize

BASE_URL = 'https://ajw.asahi.com'
DATE_FORMAT = '%B %d, %Y'

class Article(fuss.Article):

    def __init__(self, session, snippet):
        link = snippet.select('.article_title a')[0]
        super().__init__(_url_from_href(link['href']))

        self._date = strptime(snippet.select('.article_date')[0].get_text(), DATE_FORMAT)
        self._session = session

    @property
    def date(self):
        return self._date

    @property
    @memoize('_author')
    def author(self):
        self._download()
        author = self._soup.select('.author')[0]
        return author.get_text()[3:].split('/')[0].title()

    @property
    @memoize('_title')
    def title(self):
        self._download()
        return self._soup.select('#article_head h1')[0].get_text()

    @property
    @memoize('_text')
    def text(self):
        self._download()
        ps = self._soup.select('.text')[0].findAll(text = True)
        return ''.join(ps).strip()

    @memoize('_soup')
    def _download(self):
        r = self._session.get(self._url)
        if r.status_code != 200:
            msg = 'Request to {} failed with status code {}.'.format(url, r.status_code)
            raise Exception(msg)
        return BeautifulSoup(r.text, 'html.parser').select('#content')[0]

fuss.Article.register(Article)

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
            yield Article(s, div)

        if not found:
            break

        page = page + 1

def _url_from_params(params):
    return '{}/search/?{}'.format(BASE_URL, urlencode(params))

def _url_from_href(href):
    return '{}{}'.format(BASE_URL, href)

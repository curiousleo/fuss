import re
from time import strptime
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

import fuss
from wire import iswire

BASE_URL = 'https://ajw.asahi.com'
DATE_FORMAT = '%B %d, %Y'
REGEXES = {
    re.compile(r'^B. ([A-Za-z ]+)/ (AJW )?Sta(r)?ff Writer$'): fuss.Author.staff,
    re.compile(r'^B. ([A-Za-z ]+)/ Senior Staff Writer$'): (lambda name: fuss.Author.staff(name, 'senior')),
    re.compile(r'^B. ([A-Za-z ]+)/ Editorial Writer$'): (lambda name: fuss.Author.staff(name, 'editorial')),
    re.compile(r'^B. ([A-Za-z ]+)/ Columnist$'): (lambda name: fuss.Author.staff(name, 'columnist')),
    re.compile(r'^B. ([A-Za-z ]+)/ Correspondent$'): (lambda name: fuss.Author.staff(name, 'correspondent')),
    re.compile(r'^B. ([A-Za-z ]+)$'): fuss.Author.guest,
}
ASAHI_REGEX = re.compile(r'^(special to )?the as(a)?hi shimbun$')
VOX_REGEX = re.compile(r'^Vox Populi')

class Article(fuss.Article):

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def date(self):
        path = '//div[@id = "article"]/div/span[@class = "date"]/text() | ' \
               '//div[@class = "article_date"]/text()'
        date = self._etree.xpath(path)[0]
        return strptime(date.strip(), DATE_FORMAT)

    @property
    def author(self):
        selection = self._etree.xpath('//p[@class = "author"]/text()')
        if len(selection) > 0:
            return parse_author(selection[0].strip())
        else:
            return fuss.Author.unknown()

    @property
    def title(self):
        path = '//h1/text() | //div[@class = "article_title"]/text()'
        return self._etree.xpath(path)[0].strip()

    @property
    def text(self):
        path = '//div[@class = "text"]//text() | ' \
               '//div[@class = "article_summary"]//text()'
        return ''.join(p.strip() for p in self._etree.xpath(path))

    @property
    def photos(self):
        path = '//div[@class = "media_c"]/img | ' \
               '//div[@class = "photo_list"]/ul/li | ' \
               '//*[contains(concat(" ", @class, " "), " leaf ")]//img'
        return len(self._etree.xpath(path))

fuss.Article.register(Article)

def parse_author(string):
    if ASAHI_REGEX.search(string.lower()):
        return fuss.Author.staff()
    if VOX_REGEX.search(string):
        return fuss.Author.staff('Vox Populi')
    for regex, author in REGEXES.items():
        s = regex.search(string)
        if s:
            return author(s.groups(0)[0].title())
    if iswire(string):
        return fuss.Author.wire(string.title())
    return fuss.Author.unknown(string)

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

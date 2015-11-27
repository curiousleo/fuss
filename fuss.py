#! /bin/env python

from abc import ABCMeta, abstractproperty

from bs4 import BeautifulSoup
import requests

class Article(metaclass=ABCMeta):

    def __init__(self, url, session = None):
        self._url = url
        r = session.get(url) if session else requests.get(url)
        if r.status_code != 200:
            msg = 'Request to {} failed with status code {}.'.format(url, r.status_code)
            raise Exception(msg)
        self._soup = BeautifulSoup(r.text, 'html.parser')

    @property
    def url(self):
        return self._url

    @abstractproperty
    def date(self):
        pass

    @abstractproperty
    def author(self):
        pass

    @abstractproperty
    def text(self):
        pass

import argparse

import format

import asahi

sites = {
    'asahi': asahi,
}

def parser():
    from time import strptime
    date = lambda s: strptime(s, '%Y-%m-%d')

    parser = argparse.ArgumentParser()
    parser.add_argument('site', help='website name ({})'.format(', '.join(sites.keys())))
    parser.add_argument('query', help='search query (use quotes for multiple terms)')
    # parser.add_argument('-a', '--after', type=date, help='only show results published after this date (format YYYY-MM-DD)')
    # parser.add_argument('-b', '--before', type=date, help='only show results published before this date (format YYYY-MM-DD)')
    return parser

if __name__ == '__main__':
    args = parser().parse_args()
    s = requests.Session()
    site = sites[args.site]
    for url in site.find(args.query):
        print(format.cmd(site.Article(url, s)))

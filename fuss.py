#! /bin/env python

from abc import ABCMeta, abstractproperty
from os import listdir
from os.path import isfile, join
from pathlib import Path
import re
from string import punctuation

from bs4 import BeautifulSoup
import requests

class Article(metaclass=ABCMeta):

    def __init__(self, html, ident = None):
        self._ident = ident
        self._soup = BeautifulSoup(html, 'html.parser')

    @classmethod
    def from_file(cls, fname):
        with open(fname) as f:
            return cls(f.read(), str(Path(fname).absolute()))

    @classmethod
    def from_dir(cls, dname):
        fnames = (join(dname, f) for f in listdir(dname))
        fnames = filter(isfile, fnames)
        return (cls.from_file(f) for f in fnames)

    @property
    def ident(self):
        return self._ident

    @property
    def length(self):
        return len(re.findall(r'\b\w+\b', self.text))

    @abstractproperty
    def date(self):
        raise NotImplementedError

    @abstractproperty
    def author(self):
        raise NotImplementedError

    @abstractproperty
    def text(self):
        raise NotImplementedError

    @abstractproperty
    def photos(self):
        raise NotImplementedError

class Author(object):

    def __init__(self, typ, name = None, role = None):
        self.typ = typ
        self.name = name
        self.role = role

    def __str__(self):
        s = self.typ
        if self.role:
            s = s + '(' + self.role + ')'
        if self.name:
            s = s + ':' + self.name
        return s

    @classmethod
    def staff(cls, name = None, role = None):
        return cls('staff', name, role)

    @classmethod
    def guest(cls, name):
        return cls('guest', name)

    @classmethod
    def wire(cls, name):
        return cls('wire', name)

    @classmethod
    def unknown(cls, name = None):
        return cls('unknown', name)

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
        print(url)
    # with open('dump.json', 'w') as f:
        # f.write('[')
        # for url in site.find(args.query):
            # f.write(format.json(site.Article(url, s)))
            # f.write(',')
        # f.write(']')

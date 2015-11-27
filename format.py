from abc import ABCMeta, abstractmethod
from sys import stdout
from time import strftime

DATE_FORMAT = '%Y-%m-%d'

def cmd(article):
    date = strftime(DATE_FORMAT, article.date)
    return '[{}] {}'.format(date, article.title)

def csv(article):
    date = strftime(DATE_FORMAT, article.date)
    title = article.title.replace('"', '\\"')
    return '"{}","{}","{}"'.format(date, article.author, title)

from json import dumps as json_dumps
from time import strftime

DATE_FORMAT = '%Y-%m-%d'

def cmd(article):
    date = strftime(DATE_FORMAT, article.date)
    return '[{}] {}'.format(date, article.title)

def csv(article):
    date = strftime(DATE_FORMAT, article.date)
    title = article.title.replace('"', '\\"')
    return '"{}","{}","{}"'.format(date, article.author, title)

def json(article):
    date = strftime(DATE_FORMAT, article.date)
    obj = {
        'url': article.url, 'date': date, 'title': article.title,
        'author': article.author, 'text': article.text
    }
    return json_dumps(obj)

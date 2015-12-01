from json import dumps as json_dumps
from time import strftime, struct_time
from csv import writer as csv_writer

DATE_FORMAT = '%Y-%m-%d'
ARTICLE_FIELDS = ['date', 'author', 'title', 'photos', 'length']

def cmd(article):
    date = strftime(DATE_FORMAT, article.date)
    return '[{}] {}'.format(date, article.title)

def json(article):
    date = strftime(DATE_FORMAT, article.date)
    obj = {
        'url': article.url, 'date': date, 'title': article.title,
        'author': article.author, 'text': article.text
    }
    return json_dumps(obj)

def strings(article, fields):
    def stringify(prop):
        if isinstance(prop, struct_time):
            return strftime(DATE_FORMAT, prop)
        return str(prop)
    return map(lambda f: stringify(getattr(article, f)), fields)

def csv(articles, out, fields = ARTICLE_FIELDS):
    csv_writer(out).writerows(map(lambda a: strings(a, fields), articles))

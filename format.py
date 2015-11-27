from abc import ABCMeta, abstractmethod
from sys import stdout
from time import strftime

DATE_FORMAT = '%Y-%m-%d'

class Formatter(metaclass=ABCMeta):

    def __init__(self, ostream = stdout):
        assert(ostream.writable())
        self._ostream = ostream

    @abstractmethod
    def format(article):
        pass

class CmdFormatter(Formatter):

    def __init__(self, *args):
        super().__init__(*args)

    def format(self, article):
        self._ostream.write('[{}] '.format(strftime(DATE_FORMAT, article.date)))
        self._ostream.write(article.title)
        self._ostream.write('\n')

Formatter.register(CmdFormatter)

class CsvFormatter(Formatter):

    def __init__(self, *args):
        super().__init__(*args)

    def format(self, article):
        self._ostream.write('{},'.format(strftime(DATE_FORMAT, article.date)))
        self._ostream.write('{},'.format(article.author))
        self._ostream.write('"{}"'.format(article.title.replace('"', '\\"')))
        self._ostream.write('\n')

Formatter.register(CsvFormatter)

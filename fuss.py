#! /bin/env python

import argparse

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
    for article in sites[args.site].articles(args.query):
        print('{} [{}]'.format(article['title'], article['url']))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GLO-1901 AlphaVantage Cache Update Interface"""

import argparse
import datetime
import json
import requests

PARSER = argparse.ArgumentParser(
    description="GLO-1901 AlphaVantage Cache Update Interface",
    epilog="The program allows you to see the content of the cache (default option; symbol, outputsize and update date). You can update the symbols in the cache directly with the -s option.")

#PARSER.add_argument('-c', '--content', metavar='', help='See the content of the cache')
PARSER.add_argument('-s', '--symbol', type=str, metavar='symbol', nargs='+', help='Stock symbol(s) to update from AlphaVantage')
PARSER.add_argument('-o', '--outputsize', type=str, metavar='{compact,full}',
                    default='compact',
                    choices=['compact', 'full'],
                    help='The outputsize to update the specified symbols (defaults to compact)')

ARGS = PARSER.parse_args()

# AlphaVantage API info
ALPHAVANTAGE_URL = 'https://www.alphavantage.co/query'
ALPHAVANTAGE_FUNC = 'TIME_SERIES_DAILY'
ALPHAVANTAGE_API_KEY = '8QNNMQKPFWHO7VBO'


# GLO-1901 Cache API info
CACHE_INFO_URL = 'https://us-central1-glo1901vantagecache.cloudfunctions.net/infoData'
CACHE_SET_URL = 'https://us-central1-glo1901vantagecache.cloudfunctions.net/setData'
CACHE_URL = 'https://us-central1-glo1901vantagecache.cloudfunctions.net/query'

def getAlpha(symb):
    ALPHA_PARAMS = {
        'function': ALPHAVANTAGE_FUNC,
        'symbol': symb,
        'apikey': ALPHAVANTAGE_API_KEY,
        'outputsize': ARGS.outputsize,
    }
    r = requests.get(url=ALPHAVANTAGE_URL, params=ALPHA_PARAMS)
    return r.json()

def setCache(symb, data):
    CACHE_PARAMS = {'symbol': symb}
    return requests.post(url=CACHE_SET_URL, params=CACHE_PARAMS, json=data)

# Get the content of the cache
if ARGS.symbol is None:
    rep = requests.get(url=CACHE_INFO_URL)
    rep = json.loads(rep.text)

    print("|--- CACHE CONTENT ---|\n")
    for symb, meta in rep.items():
        print('{:<5}  {:>12}  {:>12}'.format(symb, meta['date'], meta['outputsize']))

else:
    for symb in ARGS.symbol:
        status = setCache(symb, getAlpha(symb))
        if not status.ok:
            print(status)
            print(status.text)
            raise AssertionError('Could not set cache symbol : ' + symb)

    print("|--- CACHE UPDATED ---|\n")
    print(*ARGS.symbol, sep='\n')


#!/usr/bin/env python

import datetime

import requests
import PyRSS2Gen
from bs4 import BeautifulSoup
from bottle import route, run, response, default_app

@route('/')
def index():
    resp = requests.get('http://mdcourts.gov/cgi-bin/indexlist.pl',
                        params={'court': 'both', 'year': 'all',
                                'order': 'bydate', 'submit': 'Submit'})

    soup = BeautifulSoup(resp.content)

    opinion_rows = soup.find_all('table')[1].find_all('tr')[1:]

    items = []
    for row in opinion_rows:
        tds = row.find_all('td')
        items.append(
            PyRSS2Gen.RSSItem(
                title = tds[4].text,
                link = row.td.find_all('a')[1]['href'],
                description = '{0} - {1}'.format(
                    tds[3].text,
                    tds[4].text,
                    ),
                guid = PyRSS2Gen.Guid(tds[0].a['href']),
                pubDate = datetime.datetime.strptime(
                    tds[2].text.strip(), '%Y-%m-%d')
                ))

    rss = PyRSS2Gen.RSS2(
        title='Maryland Appellate Court Opinions',
        description='Maryland Appellate Court Opinions',
        link=('http://mdcourts.gov/cgi-bin/indexlist.pl'
              '?court=both&year=all&order=bydate&submit=Submit'),
        lastBuildDate=datetime.datetime.now(),
        items=items)

    response.content_type = 'application/rss+xml; charset=latin9'
    return rss.to_xml()

application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=8000)

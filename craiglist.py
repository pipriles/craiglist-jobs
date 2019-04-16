#!/usr/bin/env python3 
# append this -> /d/jobs/search/jjj
# 447 cities/queries to scrape
# [ ] Implement recover protocol
# [ ] Notice when it gets banned
# [x] Config module
# [ ] Utils module
# [ ] Change data format

import requests as rq
import pandas as pd
import sys
import re
import json
import time
import gspread
import itertools
import datetime as dt
import glob
import os
import config

from bs4 import BeautifulSoup
from urllib import parse
from oauth2client.service_account import ServiceAccountCredentials

CURRENT_DIR = os.path.dirname((os.path.realpath(__file__)))

def add_scheme(url):
    if re.match(r'\w+://', url): return url
    return re.sub(r'^:?/?/?', r'http://', url)

def get_states():
    resp = rq.get('https://miami.craigslist.org/')
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h5', string='us states')
    ulist = title.find_next_sibling('ul')
    st = ulist.find_all('a')[:-1] # Delete extra more ... tag

    result = { x.get_text(strip=True): x.get('href') for x in st }
    return { k: add_scheme(v) for k, v in result.items() if v }

def fetch_cities(st_url):
    resp = rq.get(st_url)

    if not re.match(r'\w+://geo', resp.url): return { '_': resp.url }

    html = resp.text
    soup = BeautifulSoup(resp.text, 'html.parser')

    ulist  = soup.find('ul', attrs={ 'class': 'geo-site-list' })
    cities = ulist.find_all('a')

    result = { x.get_text(strip=True): x.get('href') for x in cities }
    return { k: add_scheme(v) for k, v in result.items() if v }

def fetch_urls():
    result = {}
    states = get_states()
    for name, url in states.items():
        cities = fetch_cities(url)
        print('State:', name)
        print('Cities:', len(cities))
        print('URL:', url)
        print('--------------------')
        result[name] = { 'cities': cities, 'url': url }
    return result

def cities_frame(states):
    for state, data in states.items():
        for city, url in data['cities'].items():
            yield { 'City': city, 'State': state, 'URL': url }

def scrape_jobs_page(soup):
    rows = soup.find_all('li', attrs={ 'class': 'result-row' }) 

    for row in rows:

        a = row.find('a', attrs={ 'class': 'result-title' })
        title = a.get_text(strip=True)
        href  = a.get('href')
        
        dtag = row.find('time')
        date = dtag.get('datetime')
        
        span = row.find(attrs={ 'class': 'result-hood' })
        hood = span.get_text(strip=True) if span else None
        
        span = row.find(attrs={ 'class': 'result-tags' })
        tags = span.get_text(separator=',', strip=True)
        tags = ','.join([ t.strip() for t in tags.split('\n') ])
        tags = tags.split(',')
        
        yield { 'title': title, 'url': href, 
            'date': date, 'hood': hood, 'tags': tags }

def rq_get(url, *args, **kwargs):

    cont = 2
    while cont > 0:
        try:
            resp = rq.get(url, *args, **kwargs)
            return resp
        except Exception as e:
            print('[ERROR]', e)
            cont -= 1
    raise Exception('Max retries exceeded')

def scrape_jobs(url):

    url = add_scheme(url)
    p = parse.urlparse(url)
    query = parse.parse_qs(p.query)
    query = { k: v[0] for k, v in query.items() }

    if query.get('s'):
        query['s'] = int(query['s'])
    params = query

    try:
        url = url[:url.index('?')]
    except ValueError: pass

    while True:
        # resp = rq.get(url, params=params)
        resp = rq_get(url, params=params, timeout=30)
        print(resp.url)
        
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')

        if soup.find('span', string='no results') \
        or soup.find('li', attrs={ 'class': 'result-row' }) is None:
            break
        
        page = scrape_jobs_page(soup)
        jobs = list(page)
        
        yield from jobs
        time.sleep(2)
        
        if soup.find(attrs={ 'class': 'lastpage' }): break 
        params['s'] = params.get('s', 0) + len(jobs)

def scrape_keyword(url, keyword):

    match = re.search('/(\w+)/?$', url)
    if match is None:
        fmt = '/search/jjj?query={}'.format(keyword)
    else:
        code = match.group(1)
        fmt = '/search/{}/jjj?query={}'.format(code, keyword)

    url = re.sub(r'(?:(?:/\w*/?)|/*)$', fmt, url, count=1)
    return scrape_jobs(url)

def scrape_record(record):
    data = { }
    data['url'] = record['URL']
    try:
        for k in config.KEYWORDS:
            posts = scrape_keyword(data['url'], k) 
            data[k] = list(posts) # consume posts
        return data
    except Exception:
        return None

def scrape_batch(filename):
    df = pd.read_csv(filename)
    records  = df.to_dict(orient='records')
    for row in records: 
        data = scrape_record(row)
        if data: yield data

def write_json(filename, data):
    with open(filename, 'w', encoding='utf8') as fp:
        json.dump(data, fp, indent=2)

def reformat_dict(data):

    # ugly shit
    for city in data:
        for k in config.KEYWORDS:
            for job in city[k]:
                r = job.copy()
                r['src'] = city['url']
                r['keyword'] = k
                yield r

def prepare_dataframe(data):

    if not data:
        raise Exception('No data found for dataframe')

    values = reformat_dict(data)
    df = pd.DataFrame(values)
    
    # Reorder columns
    columns = ['src', 'keyword', 'title', 'url', 'date', 'hood', 'tags']
    df = df[columns]
    
    # Rename columns
    columns = ['Source', 'Keyword', 'Title', 'URL', 'Date', 'Address', 'Tags']
    df.columns = columns
    
    # Reformat tags
    df.Tags = df.Tags.map(lambda x: ', '.join(x))   
    return df

def export_csv(filename, data):

    try:
        df = prepare_dataframe(data)
        df.to_csv(filename, index=None)
    except Exception:
        print('No data found for exporting: ignored')
    
def import_csv(filename, name):

    # Assumes csv has a header
    df = pd.read_csv(filename)
    import_df(df, name)

def import_df(df, name):

    creds = ServiceAccountCredentials.from_json_keyfile_name(
            config.CREDS_JSON, config.SCOPE)

    gc = gspread.authorize(creds)
    sh = gc.open_by_key(config.SHEET_KEY)

    today = dt.datetime.today()
    today = today.strftime('%m/%d')
    name = '{} {}'.format(name, today)

    rs, cs = df.shape
    rs += 1

    sheet = sh.add_worksheet(name, rs, cs)
    cells = sheet.range(1, 1, rs, cs)

    for cell, value in zip(cells[:cs], df.columns):
        cell.value = value

    values = itertools.chain.from_iterable(df.values)
    for cell, value in zip(cells[cs:], values):
        cell.value = '' if isinstance(value, float) else value

    sheet.update_cells(cells)

def run_city_scrape(filename):

    results = []
    cont = 1

    name = os.path.basename(filename)
    name = name.partition('.')[0]
    ofile = '{}/{}_o.csv'.format(CURRENT_DIR, name)

    try:
        fmt = '{}: [{}] {}'
        for r in scrape_batch(filename):
            ln = fmt.format(name, cont, r['url'])
            print(ln)

            results.append(r)
            export_csv(ofile, results)
            cont += 1

        # Add dataframe to the sheet
        print('Uploading results...')
        df = prepare_dataframe(results)

        code = config.US_STATES[name]

        # Split into specialist 
        name = '{} Specialist'.format(code)
        sp = df[df.Keyword.isin(config.SPECIALIST)]
        import_df(sp, name)
        
        # Split into generalist
        name = '{} General'.format(code)
        sp = df[~df.Keyword.isin(config.SPECIALIST)]
        import_df(sp, name)

    except Exception as e:
        print(e)

    finally:
        export_csv(ofile, results)

def main():
    try:
        # Assumes states are in the same folder
        path = '{}/states/*'.format(CURRENT_DIR)
        files = glob.glob(path)
        for fl in files:
            run_city_scrape(fl)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()


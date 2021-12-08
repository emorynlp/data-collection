# Copyright 2021 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Jinho D. Choi'

import glob
import json
import os
import re

import requests

RE_UNICODE = re.compile(r'[\u2019-\u2020]+')
RE_THEME = re.compile(r'https://www\.wise-sayings\.com/([a-z\-]+)-quotes/')
RE_QUOTE = re.compile(r'<blockquote>\s*<q>(.+?)</q>\s*<cite><span>(.+?)</span></cite>\s*</blockquote>')
HTML_TAGS = [('&amp;', '&'), ('&#39;', "'"), ('&#34;', "'")]
URL_404 = {
    'https://www.wisesayings.com/forever-quotes-quotes/',
    'https://www.wisesayings.com/mother-in-law-quotes-quotes/',
    'https://www.wisesayings.com/pisces-quotes-quotes/',
    'https://www.wisesayings.com/sweet-dreams-quotes-quotes/',
    'https://www.wisesayings.com/virgo-quotes-quotes/'
}


def print_stats(json_dir):
    n_themes, n_quotes = 0, 0
    for filename in sorted(glob.glob(os.path.join(json_dir, '*.json'))):
        d = json.load(open(filename))
        theme = d['theme']
        quotes = d['quotes']
        print('* [{}]({}): {}'.format(theme, 'json/{}.json'.format(theme), len(quotes)))
        n_themes += 1
        n_quotes += len(quotes)
    print(n_themes, n_quotes)


def get_quotes(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        print('Invalid URL: {}'.format(url))
        return None

    m = RE_THEME.search(url)
    if not m:
        print('Invalid Theme: {}'.format(url))
        return None

    theme = m.group(1)
    text = r.content.decode('utf-8')
    quotes = [{'quote': m.group(1).strip(), 'cite': m.group(2).strip()} for m in RE_QUOTE.finditer(text)]

    for q in quotes:
        t = q['quote']
        for o, n in HTML_TAGS:
            t = t.replace(o, n)
        if t != q['quote']:
            q['quote'] = t

    return {'source': url, 'theme': theme, 'quotes': quotes}


if __name__ == '__main__':
    # get_quotes('https://www.wisesayings.com/calculus-quotes/')
    print_stats('dat/')

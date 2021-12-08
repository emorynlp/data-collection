# ========================================================================
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
# ========================================================================

__author__ = 'Jinho D. Choi'

import json
import os
from typing import Tuple

import requests
from bs4 import BeautifulSoup

from src.aesopfables import cleanspace

HOME = 'http://read.gov/aesop/'


def extract_fable(url: str) -> Tuple[str, str]:
    html = requests.get(url).content
    top = BeautifulSoup(html, 'html.parser')
    div = top.find('div', {'id': 'page'})

    lesson = cleanspace(div.find('blockquote').get_text())
    fable = cleanspace(' '.join([p.get_text() for p in div.find_all('p')]))

    return lesson, fable


def extract(outfile: str):
    html = requests.get(os.path.join(HOME, '001.html')).content
    top = BeautifulSoup(html, 'html.parser')
    fables = []

    ul = top.find('ul', {'class': 'toc'})
    for li in ul.find_all('li'):
        a = li.find('a')
        source = os.path.join(HOME, a.get('href').strip())
        title = cleanspace(a.get_text().replace('&', 'and'))
        print(title)
        lesson, fable = extract_fable(source)
        fables.append({'source': source, 'title': title, 'lesson': lesson, 'fable': fable})

    json.dump(fables, open(outfile, 'w'), indent=2)


if __name__ == '__main__':
    extract('aesop4children.json')

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
import re
from typing import Optional, List, Dict

import requests
from bs4 import BeautifulSoup
from elit_tokenizer import EnglishTokenizer

from zzz.api import cleanspace

RE_NNNL = re.compile(r'( *\r?\n){3,}')


def extract_fable(url: str) -> Optional[str]:
    html = requests.get(url).content
    top = BeautifulSoup(html, 'html.parser')
    pre = top.find('pre')
    text = pre.get_text().strip()
    t = RE_NNNL.split(text)

    if len(t) < 3:
        print('Title missing: {}'.format(url))
        return None

    return cleanspace(t[2])


def extract_list(url: str) -> List[Dict]:
    html = requests.get(url).content
    top = BeautifulSoup(html, 'html.parser')
    table = top.find('table')
    fables = []

    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) != 2: continue

        a = tds[0].find('a')
        source = 'https://www.aesopfables.com{}'.format(a.get('href').strip())
        title = cleanspace(a.get_text())
        lesson = cleanspace(tds[1].get_text())
        if len(lesson) < 3: lesson = None
        fable = extract_fable(source)
        if fable: fables.append({'source': source, 'title': title, 'lesson': lesson, 'fable': fable})

    return fables


def extract(outfile: str):
    fables = []

    for i in range(1, 5):
        fables.extend(extract_list('https://www.aesopfables.com/aesop{}.html'.format(i)))

    # fables.sort(key=lambda d: d['title'])
    json.dump(fables, open(outfile, 'w'), indent=2)


def tokenize(infile: str, outdir: str):
    d = json.load(open(infile))
    t = EnglishTokenizer()
    nd = []

    for f in d:
        text = f['fable']
        sentence = t.decode(text)
        sentences = t.decode(text, segment=2)
        f['tokens'] = ' '.join(sentence.tokens)
        f['segments'] = [' '.join(s.tokens) for s in sentences]
        nd.append(f)

    outfile = os.path.join(outdir, os.path.basename(infile))
    json.dump(nd, open(outfile, 'w'), indent=2)


if __name__ == '__main__':
    # extract('aesopfables.json')
    # extract_list('https://www.aesopfables.com/aesop{}.html'.format(1))
    # print(extract_fable('https://www.aesopfables.com/cgi/aesop1.cgi?4&TheScorpionandtheFrog'))
    tokenize('dat/aesopfables.json', '.')
    tokenize('dat/aesopfables-alt.json', '.')
    tokenize('dat/aesop4children.json', '.')

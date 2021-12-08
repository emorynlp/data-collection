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
from typing import List, Sequence

import requests
from bs4 import BeautifulSoup

from zzz.api import cleanspace, flat_json_str_list

MCU = [
    'tt0371746',  # Iron Man (2008)
    'tt0800080',  # The Incredible Hulk (2008)
    'tt1228705',  # Iron Man 2 (2010)
    'tt0800369',  # Thor (2011)
    'tt0458339',  # Captain America: The First Avenger (2011)
    'tt0848228',  # The Avengers (2012)
    'tt1300854',  # Iron Man 3 (2013)
    'tt1981115',  # Thor: The Dark World (2013)
    'tt1843866',  # Captain America: The Winter Soldier (2014)
    'tt2015381',  # Guardians of the Galaxy (2014)
    'tt2395427',  # Avengers: Age of Ultron (2015)
    'tt0478970',  # Ant-Man (2015)
    'tt3498820',  # Captain America: Civil War (2016)
    'tt1211837',  # Doctor Strange (2016)
    'tt3896198',  # Guardians of the Galaxy Vol. 2 (2017)
    'tt2250912',  # Spider-Man: Homecoming (2017)
    'tt3501632',  # Thor: Ragnarok (2017)
    'tt1825683',  # Black Panther (2018)
    'tt4154756',  # Avengers: Infinity War (2018)
    'tt5095030',  # Ant-Man and the Wasp (2018)
    'tt4154664',  # Captain Marvel (2019)
    'tt4154796',  # Avengers: Endgame (2019)
    'tt6320628',  # Spider-Man: Far from Home (2019)
    'tt3480822',  # Black Widow (2021)
    'tt9376612',  # Shang-Chi and the Legend of the Ten Rings (2021)
    'tt9032400',  # Eternals (2021)
]

WDAS = {
    'tt0029583': 'Snow_White_and_the_Seven_Dwarfs_(1937_film)',  # 1937
    'tt0032910': 'Pinocchio_(1940_film)',  # 1940
    'tt0034091': 'The_Reluctant_Dragon_(1941_film)',  # 1941
    'tt0033563': 'Dumbo',  # 1941
    'tt0034492': 'Bambi',  # 1942
    'tt0038969': 'Song_of_the_South',  # 1946
    'tt0041094': 'The_Adventures_of_Ichabod_and_Mr._Toad',  # 1949
    'tt0042332': 'Cinderella_(1950_film)',  # 1950
    'tt0043274': 'Alice_in_Wonderland_(1951_film)',  # 1951
    'tt0046183': 'Peter_Pan_(1953_film)',  # 1953
    'tt0048280': 'Lady_and_the_Tramp',  # 1955
    'tt0053285': 'Sleeping_Beauty_(1959_film)',  # 1959
    'tt0055254': 'One_Hundred_and_One_Dalmatians',  # 1961
    'tt0057546': 'The_Sword_in_the_Stone_(1963_film)',  # 1963
    'tt0061852': 'The_Jungle_Book_(1967_film)',  # 1967
    'tt0065421': 'The_Aristocats',  # 1970
    'tt0070608': 'Robin_Hood_(1973_film)',  # 1973
    'tt0076363': 'The_Many_Adventures_of_Winnie_the_Pooh',  # 1977
    'tt0076618': 'The_Rescuers',  # 1977
    'tt0076538': 'Pete%27s_Dragon_(1977_film)',  # 1977
    'tt0082406': 'The_Fox_and_the_Hound',  # 1981
    'tt0088814': 'The_Black_Cauldron_(film)',  # 1985
    'tt0091149': 'The_Great_Mouse_Detective',  # 1986
    'tt0095776': 'Oliver_%26_Company',  # 1988
    'tt0097757': 'The_Little_Mermaid_(1989_film)',  # 1989
    'tt0100477': 'The_Rescuers_Down_Under',  # 1990
    'tt0101414': 'Beauty_and_the_Beast_(1991_film)',  # 1991
    'tt0103639': 'Aladdin_(1992_Disney_film)',  # 1992
    'tt0110357': 'The_Lion_King',  # 1994
    'tt0114148': 'Pocahontas_(1995_film)',  # 1995
    'tt0116583': 'The_Hunchback_of_Notre_Dame_(1996_film)',  # 1996
    'tt0119282': 'Hercules_(1997_film)',  # 1997
    'tt0120762': 'Mulan_(1998_film)',  # 1998
    'tt0120855': 'Tarzan_(1999_film)',  # 1999
    'tt0130623': 'Dinosaur_(film)',  # 2000
    'tt0120917': 'The_Emperor%27s_New_Groove',  # 2000
    'tt0230011': 'Atlantis:_The_Lost_Empire',  # 2001
    'tt0275847': 'Lilo_%26_Stitch',  # 2002
    'tt0133240': 'Treasure_Planet',  # 2002
    'tt0328880': 'Brother_Bear',  # 2003
    'tt0299172': 'Home_on_the_Range_(2004_film)',  # 2004
    'tt0371606': 'Chicken_Little_(2005_film)',  # 2005
    'tt0396555': 'Meet_the_Robinsons',  # 2007
    'tt0397892': 'Bolt_(2008_film)',  # 2008
    'tt0780521': 'The_Princess_and_the_Frog',  # 2009
    'tt0398286': 'Tangled',  # 2010
    'tt1449283': 'Winnie_the_Pooh_(2011_film)',  # 2011
    'tt1772341': 'Wreck-It_Ralph',  # 2012
    'tt2294629': 'Frozen_(2013_film)',  # 2013
    'tt2245084': 'Big_Hero_6_(film)',  # 2014
    'tt2948356': 'Zootopia',  # 2016
    'tt3521164': 'Moana_(2016_film)',  # 2016
    'tt5848272': 'Ralph_Breaks_the_Internet',  # 2018
    'tt4520988': 'Frozen_II',  # 2019
    'tt5109280': 'Raya_and_the_Last_Dragon',  # 2021
    # 'tt2953050': 'Encanto_(film)',                              # 2021
}


def retrieve_synopsis(imdb_id: str) -> List[str]:
    url = 'https://www.imdb.com/title/{}/plotsummary'.format(imdb_id)
    html = requests.get(url).content
    top = BeautifulSoup(html.decode('utf-8'), 'html.parser')

    synopsis = top.find('ul', {'id': 'plot-synopsis-content'})
    if not synopsis:
        print('Synopsis not found: {}'.format(imdb_id))
        return []

    return [par.strip() for li in synopsis.find_all('li', {'class': 'ipl-zebra-list__item'}) for par in li.get_text(separator='\n').split('\n')]


def retrieve_characters(imdb_id: str) -> List[str]:
    r = re.compile(r'(\(.+?\))')

    def aux(text: str):
        return ' '.join(r.sub('', text).split())

    url = 'https://www.imdb.com/title/{}/fullcredits'.format(imdb_id)
    html = requests.get(url).content
    top = BeautifulSoup(html.decode('utf-8'), 'html.parser')

    cast = top.find('table', {'class': 'cast_list'})
    if not cast:
        print('Cast list not found: {}'.format(imdb_id))
        return []

    return sorted(list({aux(a.text) for td in cast.find_all('td', {'class': 'character'}) for a in td.find_all('a')}))


def retrieve_main(imdb_id: str):
    url = 'https://www.imdb.com/title/{}'.format(imdb_id)
    html = requests.get(url).content
    top = BeautifulSoup(html.decode('utf-8'), 'html.parser')

    # title
    h1 = top.find('h1')
    title = cleanspace(h1.get_text())

    # year
    span = top.find('span', {'class': 'TitleBlockMetaData__ListItemText-sc-12ein40-2'})
    year = int(cleanspace(span.get_text()))

    # summary
    span = top.find('span', {'class': 'GenresAndPlot__TextContainerBreakpointXS_TO_M-cum89p-0 dcFkRD'})
    summary = cleanspace(span.get_text())

    # characters
    characters = retrieve_characters(imdb_id)
    synopsis = retrieve_synopsis(imdb_id)

    return {
        'source': '{}'.format(imdb_id),
        'title': title,
        'year': year,
        'summary': summary,
        'characters': characters,
        'synopsis': synopsis
    }


def retrieve_imdb(keys: Sequence[str], outdir: str):
    for key in keys:
        d = retrieve_main(key)
        print(key, d['title'])
        s = json.dumps(d, indent=2)
        s = flat_json_str_list('characters', s)
        fout = open(os.path.join(outdir, '{}.json'.format(key)), 'w')
        fout.write(s)


def extract_titles(indir: str):
    rec = []
    for filename in glob.glob(os.path.join('movie_synopses', indir, '*.json')):
        d = json.load(open(filename))
        imdb_id = os.path.basename(d['source'])
        path = '{}/{}.json'.format(indir, imdb_id)
        rec.append((d['year'], imdb_id, path, d['title']))

    for t in sorted(rec):
        print('* [`{}`]({}): {} ({})'.format(t[1], t[2], t[3], t[0]))


if __name__ == '__main__':
    retrieve_imdb(MCU, 'movie_synopses/marvel_cinematic')
    extract_titles('marvel_cinematic')

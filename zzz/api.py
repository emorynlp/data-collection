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
import re
from typing import Optional


def cleanspace(text: str) -> str:
    return ' '.join(text.split())


def flat_json_str_list(key: str, dump: str) -> Optional[str]:
    m = re.search(r'"{}": \[([\s\S]+?)]'.format(key), dump)
    if not m: return None

    start = m.start()
    end = start + len(m.group())
    items = [t for t in re.findall('"(.+?)"', m.group(1))]

    return dump[:start] + '"{}": {}'.format(key, json.dumps(items)) + dump[end:]

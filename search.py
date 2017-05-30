'''
# https://en.wikipedia.org

<script>
  (function() {
    var cx = '012954687605534514302:-ua4o780cuo';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();
</script>
<gcse:search></gcse:search>

https://cse.google.com:443/cse/publicurl?cx=012954687605534514302:-ua4o780cuo
'''

#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import logging
import urllib
import urllib.parse

import sys
import json
from collections import OrderedDict

import requests

LOG = logging.getLogger('sw.google_search')


def _decode_response(json_string):
    response = json.loads(json_string)

    meta = {key: value for key, value in response.items() if key != 'items'}
    num_results = int(meta['searchInformation']['totalResults'])
    if num_results == 0:
        LOG.info("No search results.")
        LOG.info(json.dumps(response, indent=4))
        return []
    else:
        LOG.info("{} results.".format(num_results))

    for item in response['items']:
        item['meta'] = meta

    return response['items']


def _strip_protocol(url):
    """
    >>> _strip_protocol('http://foo.bar/blah.x?baz=10&bob=15;x')
    u'foo.bar/blah.x?baz=10&bob=15;x'
    """
    p = urllib.parse.urlparse(url)
    new_url = urllib.parse.urlunparse(
        ('', p.netloc, p.path, p.params, p.query, p.fragment))
    return new_url.lstrip('/')


class GoogleCustomSearch(object):
    def __init__(self, search_engine_id, api_key):
        self.search_engine_id = search_engine_id
        self.api_key = api_key

    def search(self, keyword, site=None, max_results=100):
        assert isinstance(keyword, str)

        for start_index in range(1, max_results, 10):  # 10 is max page size
            url = self._make_url(start_index, keyword, site)
            logging.info(url)

            response = requests.get(url)
            if response.status_code == 403:
                print(response.content)
                return
            #print(response.content)

        return _decode_response(response.content.decode())

    def _make_url(self, start_index, keyword, restrict_to_site):

        if restrict_to_site is not None:
            keyword = 'site:{} {}'.format(_strip_protocol(restrict_to_site),
                                          keyword)
        # https://developers.google.com
        # /custom-search/json-api/v1/reference/cse/list
        params = OrderedDict([
            ('cx', self.search_engine_id),
            ('key', self.api_key),
            ('rsz', '10'),
            ('num', '10'),
            ('googlehost', 'www.google.com'),
            ('gss', '.com'),
            ('q', keyword),
            ('oq', keyword),
            ('filter', '0'),  # duplicate content filter, 1 | 0
            ('safe', 'off'),  # strict | moderate | off
        ])
        #if restrict_to_site is not None:
        #    params['siteSearch'] = _strip_protocol(restrict_to_site)

        return 'https://www.googleapis.com/customsearch/v1?{}'.format(
            urllib.parse.urlencode(params))


#from google_search import GoogleCustomSearch


SEARCH_ENGINE_ID = '502666-012954687605534514302:-ua4o780cuo'                           
API_KEY = 'AIzaSyDGQ6LgpJ4lFkfFevFkj2VjIOT88nEHFQQ-502666'

api = GoogleCustomSearch(SEARCH_ENGINE_ID, API_KEY)
#api.search('newton is', '')

for result in api.search('newton is', ''):
    print(result['title']) 
    print(result['link']) 
    print(result['snippet'])

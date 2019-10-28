"""
   Copyright 2017 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import hashlib
import logging

from time import time
from requests import Session

from globomap_driver_sample.settings import SSL_VERIFY


logger = logging.getLogger(__name__)


class Driver(object):

    def __init__(self):
        self.session = Session()

        self.timestamp = int(time())

    def get_data(self):
        # Sample method that retrieves data

        return {
            "Key1": "Value1",
            "Key2": "Value2"
        }

    def treat_data(self, data):
        # Sample method that parses data for loader's send method

        doc = self._make_document(data['Key1'])
        _id = hashlib.md5(bytes(str(data).lower(), 'utf-8')).hexdigest()
        key = 'sample_{}'.format(_id)
        data = self._make_data('sample_collection', 'collections', 'UPDATE', key, doc)
        return data

    # PREPARE PAYLOAD
    def _make_data(self, collection, kind, action, key, element=''):
        data = {
            'collection': collection,
            'type': kind,
            'action': action,
            'element': element,
            'key': key
        }

        return data

    def _make_document(self, data):
        _id = hashlib.md5(bytes(str(data).lower(), 'utf-8')).hexdigest()

        element = {
            'id': _id,
            'name': data,
            'provider': 'sample',
            'timestamp': self.timestamp
        }

        return element

    def _make_edge(self, origin, destiny):
        _id = hashlib.md5(bytes((str(origin) + str(destiny)).lower(), 'utf-8')).hexdigest()
        _from = hashlib.md5(bytes(str(origin).lower(), 'utf-8')).hexdigest()
        _to = hashlib.md5(bytes(str(destiny).lower(), 'utf-8')).hexdigest()
        name = '{} - {}'.format(str(origin), str(destiny))

        element = {
            'id': _id,
            'name': name,
            'provider': 'sample',
            'timestamp': self.timestamp,
            'from': 'origin_collection/sample_{}'.format(_from),
            'to': 'destiny_collection/sample_{}'.format(_to)
        }

        return element

    # REQUEST
    def _make_request(self, uri):
        request_url = '{}'.format(uri)

        try:
            response = self.session.get(
                request_url,
                verify=SSL_VERIFY,
                headers={
                    'User-Agent': 'globomap'
                }
            )
            response.encoding = 'utf-8'
        except Exception as err:
            logger.exception(
                '[SAMPLE][request] get - %s, Error:%s', request_url, err)
        else:

            status = response.status_code
            content = response.json()

            logger.debug(
                '[SAMPLE][response] get - %s %s %s',
                request_url, status, content
            )

            if status not in (200, 404):
                logger.error(
                    '[SAMPLE][error] get - %s %s %s',
                    request_url, status, content
                )
                raise GloboMapException(content)
            return content


class GloboMapException(Exception):
    pass

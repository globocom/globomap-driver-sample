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

from globomap_driver_sample.util import timed_logging
from globomap_driver_sample.settings import SSL_VERIFY


logger = logging.getLogger(__name__)


class Driver(object):

    def __init__(self):
        self.session = Session()

    @timed_logging
    def get_data(self):
        # Sample method that retrieves data in the form of a list of dicts
        # Decorator measures how long the request took and logs the method call
        # Methods that make requests via clients instead of _make_requests must
        # use this decorator

        data = []

        for i in range(1000):
            name = f"data_{str(time())}"
            data.append(
                (name, {
                    "Key1": "Value1",
                    "Key2": "Value2"
                })
            )

        return data

    def treat_data(self, data):
        # Sample method that parses data for loader's send method

        to_send = []
        for d in data:
            metadata = properties_metadata={
                            "Key1": "First Key",
                            "Key2": "Second Key"
                       }

            doc = self._make_document(d[0])
            _id = hashlib.md5(bytes(str(d[0]).lower(), 'utf-8')).hexdigest()
            doc = self._add_properties(doc, properties=d[1],
                                       properties_metadata=metadata)
            key = 'sample_{}'.format(_id)
            to_send.append(self._make_data(
                'sample_collection', 'collections', 'UPDATE', key, doc)
            )

        return to_send

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
            'timestamp': int(time())
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
            'timestamp': int(time()),
            'from': 'origin_collection/sample_{}'.format(_from),
            'to': 'destiny_collection/sample_{}'.format(_to)
        }

        return element

    def _add_properties(self, document, properties={}, properties_metadata=None):
        # Adds properties to document 'document'
        # 'properties' is a {'key': 'value'} dict
        # 'properties_metadata' is a {'key': 'Key Name'} dict

        if not properties:
            return document
        if not properties_metadata:
            properties_metadata = {}
        else:
            new_properties_metadata = {}
            for prop in properties_metadata:
                new_properties_metadata[prop] = {
                    "description": properties_metadata[prop]
                }
        for prop in [x for x in properties if x not in new_properties_metadata]:
            new_properties_metadata[prop] = { "description": prop }
        if 'properties' in document:
            document['properties'].update(properties)
            document['properties_metadata'].update(new_properties_metadata)
        else:
            document['properties'] = properties
            document['properties_metadata'] = new_properties_metadata

        return document

    # REQUEST
    @timed_logging
    def _make_request(self, uri):
        # Decorator measures how long the request took and logs the method call
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

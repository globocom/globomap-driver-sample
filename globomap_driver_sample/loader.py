"""
   Copyright 2018 Globo.com

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
import itertools
import json
import logging
import multiprocessing
from datetime import datetime
from time import time

from globomap_loader_api_client import auth
from globomap_loader_api_client.update import Update

from globomap_driver_sample import settings
from globomap_driver_sample.driver import Driver
from globomap_driver_sample.util import clear, timed_logging


class Loader(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.driver = Driver()
        auth_inst = auth.Auth(
            api_url=settings.GLOBOMAP_LOADER_API_URL,
            username=settings.GLOBOMAP_LOADER_API_USERNAME,
            password=settings.GLOBOMAP_LOADER_API_PASSWORD
        )
        Loader.update = Update(auth=auth_inst, driver_name='sample')

    @timed_logging
    def globomap_loader_post(data):
        if type(data) is dict:
            data = [data]
        for d in data:
            if 'name' in d['element']:
                Loader.logger.info(
                    'Sending message "%s %s on %s"',
                    d['action'], d['element']['name'], d['collection']
                )
            else:
                Loader.logger.info(
                    'Sending message "%s on %s"',
                    d['action'], d['collection']
                )
        return Loader.update.post(data)

    @staticmethod
    def send(data):
        try:
            res = Loader.globomap_loader_post(data)
        except Exception:
            Loader.logger.exception('Message dont sent %s', json.dumps(data))
        else:
            return res

    @timed_logging
    def run(self):
        Loader.logger.info('Driver %s started at %s',
                            self.driver, datetime.now())
        current_time = int(time())
        data = self.driver.get_data()
        payload = self.driver.treat_data(data)

        pool = multiprocessing.Pool(processes=settings.WORKERS)
        self.run_workers(pool, payload)
        self.run_clean(current_time)
        pool.close()
        Loader.logger.info('Driver %s ended at %s',
                            self.driver, datetime.now())

    def run_clean(self, current_time):
        documents = [
            clear('sample_collection', 'collections', current_time),
            clear('sample_edge', 'edges', current_time)
        ]
        self.send(documents)

    def run_workers(self, pool, data, length=100):
        for _ in pool.imap_unordered(
                self.send, self.iterator_slice(data, length)):
            pass

    def iterator_slice(self, iterator, length):
        start = 0
        end = length

        while True:
            res = list(itertools.islice(iterator, start, end))
            start += length
            end += length
            if not res:
                break
            yield res

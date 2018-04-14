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
from time import time

from globomap_loader_api_client import auth
from globomap_loader_api_client.update import Update

from globomap_driver_sample import settings
from globomap_driver_sample.driver import Driver
from globomap_driver_sample.util import clear


class Loader(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.driver = Driver()
        auth_inst = auth.Auth(
            api_url=settings.GLOBOMAP_LOADER_URL,
            username=settings.GLOBOMAP_LOADER_USERNAME,
            password=settings.GLOBOMAP_LOADER_PASSWORD
        )
        self.update = Update(auth=auth_inst, driver_name='')

    def send(self, data):
        try:
            res = self.update.post(data)
        except Exception:
            self.logger.exception('Message dont sent %s', json.dumps(data))
        else:
            return res

    def run(self):
        current_time = int(time())
        data = self.driver.get_data()

        pool = multiprocessing.Pool(processes=settings.WORKERS)
        self.run_workers(pool, data)
        self.run_clean(current_time)
        pool.close()

    def run_clean(self, current_time):
        documents = [
            clear('zabbix_graph', 'collections', current_time),
            clear('zabbix_link', 'edges', current_time)
        ]
        self.send(documents)

    def run_workers(self, pool, data, length=100):

        storage_cursor = self.driver.treat_data(data)
        for _ in pool.imap_unordered(
                self.send, self.iterator_slice(storage_cursor, length)):
            pass

    def iterator_slice(self, iterator, length):
        while True:
            res = list(itertools.islice(iterator, length))

            if not res:
                break
            yield res

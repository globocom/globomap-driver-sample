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

import datetime
import logging


def timed_logging(func, *args, **kwargs):
    logger = logging.getLogger('timed_logging')

    def inner_func(*args, **kwargs):
        init_time = datetime.datetime.now()
        ret = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        duration = str(end_time - init_time)

        strargs = str(args)
        if len(strargs) > 500:
            strargs = strargs[:245] + \
                      " [...] " + \
                      strargs[-245:]

        logger.info(
            'Function "%s" with args %s completed in %s',
            func.__name__, strargs, duration
        )

        return ret
    return inner_func


def clear(collection, type, timestamp):
    data = {
        'action': 'CLEAR',
        'collection': collection,
        'type': type,
        'element': [[{'field': 'timestamp', 'value': timestamp, 'operator': '<'}]]
    }
    return data

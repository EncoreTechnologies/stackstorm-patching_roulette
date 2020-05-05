#!/usr/bin/env python
# Copyright 2020 Encore Technologies
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
from st2common.runners.base_action import Action
import datetime
import json
import random


class Spin(Action):
    def __init__(self, config):
        super(Spin, self).__init__(config)

    def run(self, members, assignments):
        random.shuffle(members)
        random.shuffle(assignments)

        results = []
        len_members = len(members)
        len_assignments = len(assignments)
        len_max = max(len_members, len_assignments)
        for i in range(0, len_max):
            # if we have more members than assignments, then assign the members at the end byes!
            if i < len_assignments:
                assignment = assignments[i % len_assignments]
            else:
                assignment = 'bye'
            results.append({'member': members[i % len_members],
                            'assignment': assignment})

        # sort results by member
        results = sorted(results, key=lambda r: r['member'])

        data = {
            'date': datetime.datetime.now().isoformat(),
            'results': results,
        }

        # Add a results to the datastore
        self.action_service.set_value(name='patching_roulette.results', value=json.dumps(data))
        return data

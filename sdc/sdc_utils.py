# Copyright 2018 Sysdig
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


def are_jsons_equal(json1, json2):
    def ordered(o):
        if isinstance(o, dict):
            return sorted((k, ordered(v)) for k, v in o.items())
        if isinstance(o, list):
            return sorted(ordered(x) for x in o)
        else:
            return o

    return ordered(json1) == ordered(json2)

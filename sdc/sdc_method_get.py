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

from sdcclient import SdMonitorClient
from typing import AnyStr, List
import json
import yaml

from sdc.sdc_enums import EXIT_CODES


def get_dashboards(sdmonitor: SdMonitorClient, ids: List, format: AnyStr):
    ok, data = sdmonitor.get_dashboards()
    ids = set([str(id) for id in ids])
    if not ok:
        print(data)
        return EXIT_CODES.ERR_METHOD_NOT_FOUND

    dashboards = [dash for dash in data["dashboards"] if str(dash["id"]) in ids]
    if len(dashboards) == 0:
        print("No dashboards found with these IDs")
        return EXIT_CODES.ERR_METHOD_NOT_FOUND

    if format == "yaml":
        print(yaml.dump(dashboards))
        return EXIT_CODES.OK

    print(json.dumps(dashboards, indent=2))

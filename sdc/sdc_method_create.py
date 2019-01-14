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

from typing import List, AnyStr, Any
from sdcclient import SdMonitorClient, SdSecureClient
from sdc.sdc_enums import EXIT_CODES
import json
import yaml


def create_user(sdmonitor: SdMonitorClient, email, first_name, last_name, system_role="ROLE_USER"):
    ok, res = sdmonitor.create_user_invite(user_email=email, first_name=first_name, last_name=last_name,
                                           system_role=system_role)
    if not ok:
        print("error creating the user: ", res)
        return EXIT_CODES.ERR_CREATING_USER

    return EXIT_CODES.OK


def create_dashboards_from_file(sdmonitor: SdMonitorClient, file: Any):
    contents = file.read()
    try:
        dashboards = json.loads(contents)
        for dboard in dashboards:
            dboard['timeMode'] = {'mode': 1}
            dboard['time'] = {'last': 2 * 60 * 60 * 1000000, 'sampling': 2 * 60 * 60 * 1000000}
            ok, res = sdmonitor.create_dashboard_from_template(dboard["name"], dboard, shared=dboard["isShared"])
            if not ok:
                print(f"Error creating the dashboard {dboard['name']}: {res}")
                return EXIT_CODES.ERR_CREATING_DASHBOARD
            print(f"Created dashboard {dboard['name']}")
        return EXIT_CODES.OK
    except:
        pass

    try:
        dashboards = yaml.load(contents)
        for dboard in dashboards:
            dboard['timeMode'] = {'mode': 1}
            dboard['time'] = {'last': 2 * 60 * 60 * 1000000, 'sampling': 2 * 60 * 60 * 1000000}
            ok, res = sdmonitor.create_dashboard_from_template(dboard["name"], dboard, shared=dboard["isShared"])
            if not ok:
                print(f"Error creating the dashboard {dboard['name']}: {res}")
                return EXIT_CODES.ERR_CREATING_DASHBOARD
            print(f"Created dashboard {dboard['name']}")
        return EXIT_CODES.OK
    except:
        pass
    return EXIT_CODES.ERR_CREATING_DASHBOARD

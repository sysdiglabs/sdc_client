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

from sdcclient import SdMonitorClient, SdSecureClient
from typing import AnyStr, List

from sdc.sdc_enums import EXIT_CODES


def delete_user(sdmonitor: SdMonitorClient, email: AnyStr):
    ok, res = sdmonitor.delete_user(user_email=email)
    if not ok:
        print("error deleting the user: ", res)
        return EXIT_CODES.ERR_DELETING_USER

    return EXIT_CODES.OK


def delete_dashboards(sdmonitor: SdMonitorClient, ids: List):
    for id in ids:
        ok, res = sdmonitor.delete_dashboard(dashboard={"id": id})
        if not ok:
            print(f"error deleting the dashboard {id}: {res}")
            return EXIT_CODES.ERR_DELETING_DASHBOARD
        print(f"Deleted dashboard {id}")
    return EXIT_CODES.OK


def delete_policies(sdsecure: SdSecureClient, ids: List):
    for id in ids:
        ok, res = sdsecure.delete_policy_id(id=id)
        if not ok:
            print(f"error deleting the policy {id}: {res}")
            return EXIT_CODES.ERR_DELETING_POLICY
        print(f"Deleted policy {id}")
    return EXIT_CODES.OK

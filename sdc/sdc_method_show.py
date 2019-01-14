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

from sdc.sdc_enums import EXIT_CODES
from sdc.sdc_extend import SdMonitorClient, SdSecureClient


def show_users(sdmonitor: SdMonitorClient):
    ok, data = sdmonitor.get_users()
    if not ok:
        print(data)
        return EXIT_CODES.ERR_METHOD_NOT_FOUND

    print("%-6s %-38s %-13s %-15s %-7s" % ("ID", "USERNAME", "FIRSTNAME", "LASTNAME", "ACTIVE"))
    for user in data:
        print("%-6d %-38s %-13s %-15s %-7s" % (user['id'], user['username'], user['firstName'], user['lastName'],
                                               'enabled' if user['enabled'] else 'disabled'))
    return EXIT_CODES.OK


def show_dashboards(sdmonitor: SdMonitorClient):
    ok, data = sdmonitor.get_dashboards()
    if not ok:
        print(data)
        return EXIT_CODES.ERR_METHOD_NOT_FOUND

    print("%-6s %-48s %-38s %-15s %-7s %-7s" % ("ID", "NAME", "USER", "AUTOCREATED", "SHARED", "PUBLIC"))
    for dashboard in data['dashboards']:
        print("%-6d %-48s %-38s %-15s %-7s %-7s" % (dashboard['id'],
                                                    dashboard['name'].strip(),
                                                    dashboard['username'].strip(),
                                                    'yes' if dashboard['autoCreated'] else 'no',
                                                    'yes' if dashboard['isShared'] else 'no',
                                                    'yes' if dashboard['isPublic'] else 'no'))
    return EXIT_CODES.OK


def show_policies(sdsecure: SdSecureClient):
    ok, data = sdsecure.list_policies()
    if not ok:
        print(data)
        return EXIT_CODES.ERR_METHOD_NOT_FOUND

    print("%-6s %-100s %-8s %-15s %-7s" % ("ID", "NAME", "SEVERITY", "AUTOCREATED", "NOTIFICATION"))
    for policy in data['policies']:
        print("%-6d %-100s %-8s %-15s %-7s" % (policy['id'],
                                              policy['name'].strip(),
                                              policy['severity'],
                                              'yes' if policy['isBuiltin'] else 'no',
                                              len(policy['notificationChannelIds'])))
    return EXIT_CODES.OK

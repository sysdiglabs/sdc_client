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

import os
from sdc.sdc_extend import SdSecureClient, SdMonitorClient
from typing import AnyStr

from sdc.sdc_enums import BACKUP_RESTORE_FILES, EXIT_CODES


def restore_monitor(sdmonitor: SdMonitorClient, path: AnyStr, all_users: bool = False):
    sdmonitor.drop_dashboards()
    ok, res = sdmonitor.restore_dashboards_from(os.path.join(path, BACKUP_RESTORE_FILES.DASHBOARDS),
                                                fromAllUsers=all_users)
    if not ok:
        print('Error restoring dashboards: ', res)
        return EXIT_CODES.ERR_RESTORING_DASHBOARDS

    sdmonitor.drop_alerts()
    sdmonitor.drop_notification_channels()

    ok, res = sdmonitor.restore_notification_channels_from(
        os.path.join(path, BACKUP_RESTORE_FILES.NOTIFICATION_CHANNELS))
    if not ok:
        print('Error restoring notification channels: ', res)
        return EXIT_CODES.ERR_RESTORING_NOTIFICATION_CHANNELS

    changed_ids = res

    ok, res = sdmonitor.restore_alerts_from(os.path.join(path, BACKUP_RESTORE_FILES.ALERTS), changed_ids)
    if not ok:
        print('Error restoring alerts: ', res)
        return EXIT_CODES.ERR_RESTORING_ALERTS

    ok, res = sdmonitor.restore_users_from(os.path.join(path, BACKUP_RESTORE_FILES.USERS))
    if not ok:
        print('Error restring users: ', res)
        return EXIT_CODES.ERR_RESTORING_USERS

    ok, res = sdmonitor.restore_teams_from(os.path.join(path, BACKUP_RESTORE_FILES.TEAMS_MONITOR))
    if not ok:
        print('Error restoring monitor teams: ', res)
        return EXIT_CODES.ERR_RESTORING_TEAMS

    return EXIT_CODES.OK


def restore_secure(sdsecure: SdSecureClient, path: AnyStr):
    sdsecure.drop_policies()
    ok, res = sdsecure.restore_policies_from(os.path.join(path, BACKUP_RESTORE_FILES.POLICIES))
    if not ok:
        print('Error restoring policies: ', res)
        return EXIT_CODES.ERR_RESTORING_POLICIES

    ok, res = sdsecure.restore_teams_from(os.path.join(path, BACKUP_RESTORE_FILES.TEAMS_SECURE))
    if not ok:
        print('Error restoring monitor teams: ', res)
        return EXIT_CODES.ERR_RESTORING_TEAMS

    ok, res = sdsecure.restore_user_falco_rules_from(os.path.join(path, BACKUP_RESTORE_FILES.USER_FALCO_RULES))
    if not ok:
        print('Error restoring user falco rules: ', res)
        return EXIT_CODES.ERR_RESTORING_FALCO_USER_RULES

    return EXIT_CODES.OK

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
from .sdc_extend import SdMonitorClient, SdSecureClient
from typing import AnyStr

from sdc.sdc_enums import BACKUP_RESTORE_FILES, EXIT_CODES


def backup_monitor(sdmonitor: SdMonitorClient, path: AnyStr):
    ok, res = sdmonitor.save_dashboards_to(os.path.join(path, BACKUP_RESTORE_FILES.DASHBOARDS))
    if not ok:
        print('Error saving dashboards: ', res)
        return EXIT_CODES.ERR_SAVING_DASHBOARDS

    ok, res = sdmonitor.save_alerts_to(os.path.join(path, BACKUP_RESTORE_FILES.ALERTS))
    if not ok:
        print('Error saving alerts: ', res)
        return EXIT_CODES.ERR_SAVING_ALERTS

    ok, res = sdmonitor.save_users_to(os.path.join(path, BACKUP_RESTORE_FILES.USERS))
    if not ok:
        print('Error saving monitor users: ', res)
        return EXIT_CODES.ERR_SAVING_USERS

    ok, res = sdmonitor.save_teams_to(os.path.join(path, BACKUP_RESTORE_FILES.TEAMS_MONITOR))
    if not ok:
        print('Error saving monitor teams: ', res)
        return EXIT_CODES.ERR_SAVING_TEAMS

    ok, res = sdmonitor.save_notification_channels_to(os.path.join(path, BACKUP_RESTORE_FILES.NOTIFICATION_CHANNELS))
    if not ok:
        print('Error saving notification channels: ', res)
        return EXIT_CODES.ERR_SAVING_NOTIFICATION_CHANNELS

    return EXIT_CODES.OK


def backup_secure(sdsecure: SdSecureClient, path: AnyStr):
    ok, res = sdsecure.save_policies_to(os.path.join(path, BACKUP_RESTORE_FILES.POLICIES))
    if not ok:
        print('Error saving policies: ', res)
        return EXIT_CODES.ERR_SAVING_POLICIES

    ok, res = sdsecure.save_teams_to(os.path.join(path, BACKUP_RESTORE_FILES.TEAMS_SECURE))
    if not ok:
        print('Error saving secure teams: ', res)
        return EXIT_CODES.ERR_SAVING_TEAMS

    ok, res = sdsecure.save_user_falco_rules_to(os.path.join(path, BACKUP_RESTORE_FILES.USER_FALCO_RULES))
    if not ok:
        print('Error saving user falco rules: ', res)
        return EXIT_CODES.ERR_SAVING_FALCO_USER_RULES

    return EXIT_CODES.OK

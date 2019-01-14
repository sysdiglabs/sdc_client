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

from .sdc_extend import SdMonitorClient, SdSecureClient
from typing import AnyStr
from sdc.sdc_enums import BACKUP_RESTORE_FILES, EXIT_CODES
import sdc.sdc_utils as utils
import os
import json


def check_dashboards(sdmonitor: SdMonitorClient, path: AnyStr) -> bool:
    something_changed = False

    with open(os.path.join(path, BACKUP_RESTORE_FILES.DASHBOARDS)) as dashboards_file:
        ok, remote_dashboards = sdmonitor.get_dashboards()
        if not ok:
            raise Exception("error retrieving the dashboards")

        local_dashboards = json.load(dashboards_file)
        equal = utils.are_jsons_equal(remote_dashboards, local_dashboards)

        if not equal:
            something_changed = True
            print("dashboards differ")
        else:
            print("dashboards are the same")

    return something_changed


def check_alerts(monitor: SdMonitorClient, path: AnyStr) -> bool:
    something_changed = False

    with open(os.path.join(path, BACKUP_RESTORE_FILES.ALERTS)) as alerts_file:
        ok, remote_alerts = monitor.get_alerts()
        if not ok:
            raise Exception("error retrieving the alerts")

        local_alerts = json.load(alerts_file)
        equal = utils.are_jsons_equal(local_alerts, remote_alerts)
        if not equal:
            something_changed = True
            print("alerts differ")
        else:
            print("alerts are the same")

    return something_changed


def check_users(monitor: SdMonitorClient, path: AnyStr) -> bool:
    something_changed = False

    with open(os.path.join(path, BACKUP_RESTORE_FILES.USERS)) as users_file:
        ok, remote_users = monitor.get_users()
        if not ok:
            raise Exception("could not retrieve users")

        local_users = json.load(users_file)
        equal = utils.are_jsons_equal(local_users, remote_users)

        if not equal:
            something_changed = True
            print("users differ")
        else:
            print("users are the same")

    return something_changed


def check_teams_monitor(monitor: SdMonitorClient, path: AnyStr) -> bool:
    something_changed = False

    with open(os.path.join(path, BACKUP_RESTORE_FILES.TEAMS_MONITOR)) as teams_file:
        ok, remote_teams = monitor.get_all_teams()
        if not ok:
            raise Exception("could not retrieve teams")

        local_teams = json.load(teams_file)
        equal = utils.are_jsons_equal(local_teams, remote_teams)

        if not equal:
            something_changed = True
            print("teams differ")
        else:
            print("teams are the same")

    return something_changed


def check_notification_channels(monitor: SdMonitorClient, path: AnyStr) -> bool:
    something_changed = False

    with open(os.path.join(path, BACKUP_RESTORE_FILES.NOTIFICATION_CHANNELS)) as notification_channels_file:
        ok, remote_notification_channels = monitor.get_notification_channels()
        if not ok:
            raise Exception("could not retrieve notification channels")

        local_notification_channels = json.load(notification_channels_file)
        equal = utils.are_jsons_equal(local_notification_channels, remote_notification_channels)

        if not equal:
            something_changed = True
            print("notification channels differ")
        else:
            print("notification channels are the same")

    return something_changed


def check_monitor(sdmonitor: SdMonitorClient, path: AnyStr) -> bool:
    something_changed = check_dashboards(sdmonitor, path)
    something_changed = check_alerts(sdmonitor, path) or something_changed
    something_changed = check_users(sdmonitor, path) or something_changed
    something_changed = check_teams_monitor(sdmonitor, path) or something_changed
    something_changed = check_notification_channels(sdmonitor, path) or something_changed

    if something_changed:
        print("Monitor remote state has changed somehow")

    return something_changed


def check_policies(sdsecure: SdSecureClient, path: AnyStr) -> bool:
    something_changed = False
    with open(os.path.join(path, BACKUP_RESTORE_FILES.POLICIES)) as policies_file:
        ok, remote_policies = sdsecure.list_policies()
        if not ok:
            raise Exception("unable to retrieve policies")

        local_policies = json.load(policies_file)
        equal = utils.are_jsons_equal(local_policies, remote_policies)

        if not equal:
            something_changed = True
            print("policies differ")
        else:
            print("policies are the same")

    return something_changed


def check_teams_secure(sdsecure: SdSecureClient, path: AnyStr) -> bool:
    something_changed = False

    with open(os.path.join(path, BACKUP_RESTORE_FILES.TEAMS_SECURE)) as teams_file:
        ok, remote_teams = sdsecure.get_all_teams()
        if not ok:
            raise Exception("could not retrieve teams")

        local_teams = json.load(teams_file)
        equal = utils.are_jsons_equal(local_teams, remote_teams)

        if not equal:
            something_changed = True
            print("teams differ")
        else:
            print("teams are the same")

    return something_changed


def check_user_falco_rules(sdsecure: SdSecureClient, path: AnyStr) -> bool:
    something_changed = False

    with open(os.path.join(path, BACKUP_RESTORE_FILES.USER_FALCO_RULES)) as falco_rules_file:
        ok, remote_falco_rules = sdsecure.get_user_falco_rules()
        if not ok:
            raise Exception("could not retrieve user falco rules")

        local_falco_rules = json.load(falco_rules_file)
        equal = utils.are_jsons_equal(local_falco_rules, remote_falco_rules)

        if not equal:
            something_changed = True
            print("falco rules differ")
        else:
            print("falco rules are the same")

    return something_changed


def check_secure(sdsecure: SdSecureClient, path: AnyStr) -> bool:
    something_changed = check_policies(sdsecure, path)
    something_changed = check_teams_secure(sdsecure, path) or something_changed
    something_changed = check_user_falco_rules(sdsecure, path) or something_changed

    if something_changed:
        print("Monitor remote state has changed somehow")

    return something_changed

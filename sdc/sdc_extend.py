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

import json
from typing import Union, List, Optional, AnyStr

import requests
from sdcclient import SdMonitorClient, SdSecureClient
from sdcclient._client import _SdcCommon as SdcCommon


def drop_dashboards(self: SdMonitorClient):
    ok, data = self.get_dashboards()
    if ok:
        ok, userdata = self.get_user_info()
        if ok:
            username = userdata["user"]["username"]
            res = []
            dashboards = [dboard for dboard in data['dashboards'] if
                          "username" in dboard and dboard["username"] == username]
            total = len(dashboards)
            for i, dashboard in enumerate(dashboards):
                print(f"[{i + 1}/{total}] Removing dashboard {dashboard['name'].strip()}... ", end="", flush=True)
                removed, err = self.delete_dashboard(dashboard)
                if removed:
                    print("OK")
                    res.append(dashboard)
                else:
                    print("ERROR")
            return [True, res]
        else:
            return [False, userdata]
    else:
        return [False, data]


def restore_dashboards_from(self: SdMonitorClient, filename: AnyStr, fromAllUsers: bool = False) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]], List[object]]:
    with open(filename) as file:
        file_data = json.load(file)
        errors = []
        ok, userdata = self.get_user_info()
        if ok:
            username = userdata["user"]["username"]
            dashboards = [dboard for dboard in file_data["dashboards"] if
                          fromAllUsers or "username" in dboard and dboard["username"] == username]
            total = len(dashboards)
            for i, dashboard in enumerate(dashboards):
                print(f"[{i + 1}/{total}] Creating dashboard {dashboard['name'].strip()}... ", end="", flush=True)
                dashboard['id'] = None
                dashboard['version'] = None
                dashboard['schema'] = 1
                ok, result = self.create_dashboard_with_configuration(dashboard)
                if not ok:
                    print("ERROR")
                    errors.append("couldn't recreate dashboard " + dashboard['name'] + ': ' + result)
                else:
                    print("OK")

            if len(errors) != 0:
                return [False, errors]
            else:
                return [True, None]
        else:
            return [False, userdata]


def save_dashboards_to(self: SdMonitorClient, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename, 'w') as file:
        success, data = self.get_dashboards()
        if success:
            data['dashboards'].sort(key=lambda dashboard: dashboard['id'])
            json.dump(data, file, sort_keys=True, indent=2)
            print('Saved dashboards to %s' % filename)
            return [True, None]
        else:
            return [False, data]


def drop_alerts(self: SdMonitorClient):
    ok, data = self.get_alerts()
    if ok:
        res = []
        total = len(data['alerts'])
        for i, alert in enumerate(data['alerts']):
            print(f"[{i + 1}/{total}] Removing alert {alert['name'].strip()}...")
            removed, err = self.delete_alert(alert)
            if removed:
                res.append(alert)
            else:
                print(err)
        return [True, res]
    else:
        return [False, data]


def restore_alerts_from(self: SdMonitorClient, filename: AnyStr, changed_ids=None, remove_notification_channels=False) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename) as file:
        file_data = json.load(file)
        errors = []
        total = len(file_data['alerts'])
        for i, alert in enumerate(file_data['alerts']):
            print(f"[{i + 1}/{total}] Creating alert {alert['name'].strip()}... ", end="", flush=True)

            # Modify the old Ids with the new ones if they are provided
            if changed_ids is not None:
                if "notificationChannelIds" in alert:
                    changedListKeys = list(changed_ids.keys())
                    for indexOldId, oldId in enumerate(alert["notificationChannelIds"]):
                        for id in changedListKeys:
                            if int(id) == oldId:
                                alert["notificationChannelIds"][indexOldId] = int(changed_ids[id])

            if remove_notification_channels:
                alert["notificationChannelIds"] = []

            ok, result = self.create_alert(alert_obj=alert)
            if not ok:
                print("ERROR")
                errors.append("couldn't recreate alert " + alert['name'] + ': ' + result)
            else:
                print("OK")
        if len(errors) != 0:
            return [False, errors]
        else:
            return [True, None]


def save_alerts_to(self: SdMonitorClient, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename, 'w') as file:
        success, data = self.get_alerts()
        if success:
            data['alerts'].sort(key=lambda alert: alert['id'])
            json.dump(data, file, sort_keys=True, indent=2)
            print('Saved alerts to %s' % filename)
            return [True, None]
        else:
            return [False, data]


def save_users_to(self: SdcCommon, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename, 'w') as file:
        success, data = self.get_users()
        if success:
            data.sort(key=lambda user: user['id'])
            json.dump(data, file, sort_keys=True, indent=2)
            print('Saved users to %s' % filename)
            return [True, None]
        else:
            return [False, data]


def restore_users_from(self: SdcCommon, filename: AnyStr):
    '''
    Restores users without dropping the existing ones
    '''
    with open(filename) as file:
        file_data = json.load(file)

        existing_user_list = []
        ok, data = self.get_users()
        if ok:
            existing_user_list = [user["username"] for user in data]
        else:
            return [False, data]

        errors = []
        users = [user for user in file_data if not user["username"] in existing_user_list]
        total = len(users)
        for i, user in enumerate(users):
            print(f"[{i + 1}/{total}] Creating user {user['username']}... ", end="", flush=True)
            ok, res = self.create_user_invite(user["username"], user["firstName"], user["lastName"],
                                              user["systemRole"])
            if not ok:
                print("ERROR")
                errors.append("couldn't recreate user " + user["username"] + " : " + res)
            else:
                print("OK")

        if len(errors) != 0:
            return [False, errors]
        else:
            return [True, None]


def drop_policies(self: SdSecureClient):
    ok, data = self.list_policies()
    if ok:
        res = []
        total = len(data['policies'])
        for i, policy in enumerate(data['policies']):
            print(f"[{i + 1}/{total}] Removing policy {policy['name']}... ", end="", flush=True)
            removed, err = self.delete_policy_id(policy['id'])
            if removed:
                print("OK")
                res.append(policy)
            else:
                print("ERROR")
        return [True, res]
    else:
        return [False, data]


def restore_policies_from(self: SdSecureClient, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename) as file:
        file_data = json.load(file)
        errors = []
        total = len(file_data['policies'])
        for i, policy in enumerate(file_data['policies']):
            print(f"[{i + 1}/{total}] Creating policy {policy['name']}... ", end="", flush=True)
            policy['id'] = None
            policy['version'] = None
            policy['schema'] = 1
            ok, result = self.add_policy(json.dumps(policy))
            if not ok:
                print("ERROR")
                errors.append("couldn't recreate policy " + policy['name'] + ': ' + result)
            else:
                print("OK")
        if len(errors) != 0:
            return [False, errors]
        else:
            return [True, None]


def save_policies_to(self: SdSecureClient, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename, 'w') as file:
        success, data = self.list_policies()
        if success:
            data['policies'].sort(key=lambda policy: policy['id'])
            json.dump(data, file, sort_keys=True, indent=2)
            print('Saved policies to %s' % filename)
            return [True, None]
        else:
            return [False, data]


# TODO Make a pull request to have this method in the official client
def get_all_teams(self: SdcCommon) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    res = requests.get(self.url + '/api/teams', headers=self.hdrs, verify=self.ssl_verify)
    if not self._checkResponse(res):
        return [False, self.lasterr]
    return [True, res.json()]


def drop_teams(self: SdcCommon):
    ok, data = self.get_all_teams()
    if ok:
        res = []
        total = len(data['teams'])
        for i, team in enumerate(data['teams']):
            if not team["immutable"]:
                print(f"[{i+1}/{total}] Removing team {team['name']}...")
                removed, err = self.delete_team(team['name'])
                if removed:
                    res.append(team)
        return [True, res]
    else:
        return [False, data]


def restore_teams_from(self: SdcCommon, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename) as file:
        file_data = json.load(file)
        errors = []
        total = len(file_data['teams'])
        for i, team in enumerate(file_data['teams']):
            if not team["immutable"]:
                print(f"[{i+1}/{total}] Creating team {team['name']}")
                memberships = {member['userName']: member['role'] for member in team['userRoles']}
                filter = team['filter'] if 'filter' in team else ''
                description = team['description'] if 'description' in team else ''
                ok, result = self.create_team(team['name'], memberships, filter, description, team['show'],
                                              team['theme'], team['canUseSysdigCapture'], team['canUseCustomEvents'],
                                              team['canUseAwsMetrics'])
                if not ok:
                    if "409" in result:  # Team already existing, not an error
                        print("Team " + team['name'] + " already exists")
                        continue
                    errors.append("couldn't recreate team " + team['name'] + ': ' + result)
        if len(errors) != 0:
            return [False, errors]
        else:
            return [True, None]


def save_teams_to(self: SdcCommon, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename, 'w') as file:
        success, data = self.get_all_teams()
        if success:
            data['teams'].sort(key=lambda team: team['id'])
            json.dump(data, file, sort_keys=True, indent=2)
            print('Saved teams to %s' % filename)
            return [True, None]
        else:
            return [False, data]


def save_notification_channels_to(self: SdMonitorClient, filename: AnyStr):
    with open(filename, 'w') as file:
        success, data = self.get_notification_channels()
        if success:
            data.sort(key=lambda nc: nc['id'])
            json.dump(data, file, sort_keys=True, indent=2)
            print('Saved notification_channels to %s' % filename)
            return [True, None]
        else:
            return [False, data]


def drop_notification_channels(self: SdMonitorClient):
    ok, data = self.get_notification_channels()
    if ok:
        res = []
        total = len(data)
        for i, channel in enumerate(data):
            print(f"[{i + 1}/{total}] Removing notification channel {channel['name']} of type {channel['type']} and "
                  f"ID {channel['id']}...", end="", flush=True)
            removed, err = self.delete_notification_channel(channel)
            if removed:
                print("OK")
                res.append(channel)
            else:
                print("ERROR")
        return [True, res]
    else:
        return [False, data]


def restore_notification_channels_from(self: SdMonitorClient, filename: AnyStr):
    with open(filename) as file:
        file_data = json.load(file)
        errors = []
        ids_changed = {}
        total = len(file_data)
        for i, channel in enumerate(file_data):
            id = channel["id"]
            name = channel["name"] if "name" in channel else ""
            type = channel["type"] if "type" in channel else ""
            print(f"[{i + 1}/{total}] Creating notification channel {name} of type {type}... ", end="", flush=True)

            ok, result = self.create_notification_channel(channel)
            if not ok:
                print("ERROR")
                errors.append("couldn't recreate team " + channel['name'] + ': ' + result)
            else:
                print("OK")
                ids_changed[str(id)] = str(result["notificationChannel"]["id"])
        if len(errors) != 0:
            return [False, errors]
        else:
            return [True, ids_changed]


# TODO Make a pull request to have this method in the official client
def get_notification_channels(self: SdcCommon):
    res = requests.get(self.url + '/api/notificationChannels/', headers=self.hdrs, verify=self.ssl_verify)
    if not self._checkResponse(res):
        return [False, self.lasterr]
    return [True, res.json()['notificationChannels']]


# TODO Make a pull request to have this method in the official client
def create_notification_channel(self: SdcCommon, channel):
    channel["id"] = None
    channel["version"] = None
    channel["createdOn"] = None
    channel["modifiedOn"] = None
    channel_json = {
        'notificationChannel': channel
    }

    res = requests.post(self.url + '/api/notificationChannels', headers=self.hdrs, data=json.dumps(channel_json),
                        verify=self.ssl_verify)
    if not self._checkResponse(res):
        return [False, self.lasterr]
    return [True, res.json()]


# TODO Remove this function once the official sdcclient becomes fully compatible with Python 3
def delete_user(self: SdcCommon, user_email: AnyStr) \
        -> Union[List[Union[bool, str]], List[Union[bool, dict]], List[bool]]:
    """**Description**
        Deletes a user from Sysdig Monitor. Compatible with Python 3.

    **Arguments**
        - **user_email**: the email address of the user that will be deleted from Sysdig Monitor

    **Example**
        `examples/user_team_mgmt.py <https://github.com/draios/python-sdc-client/blob/master/examples/user_team_mgmt.py>`_
    """
    res = self.get_user_ids([user_email])
    if not res[0]:
        return res
    userid = list(res[1])[0]
    res = requests.delete(self.url + '/api/users/' + str(userid), headers=self.hdrs, verify=self.ssl_verify)
    if not self._checkResponse(res):
        return [False, self.lasterr]
    return [True, None]


def save_user_falco_rules_to(self: SdSecureClient, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename, 'w') as file:
        success, data = self.get_user_falco_rules()
        if success:
            json.dump(data, file, sort_keys=True, indent=2)
            print('Saved user falco rules to %s' % filename)
            return [True, None]
        else:
            return [False, data]


def restore_user_falco_rules_from(self: SdSecureClient, filename: AnyStr) -> Union[
    List[Union[bool, str]], List[Union[bool, dict]], List[bool], List[Optional[bool]]]:
    with open(filename) as file:
        file_data = json.load(file)
        print('Restoring user falco rules...')
        ok, result = self.set_user_falco_rules(file_data["userRulesFile"]["content"])
        if not ok:
            return [False, result]
        return [True, None]


# TODO Remove this function once the official sdcclient becomes fully compatible with Python 3
def create_team(self, name, memberships=None, filter='', description='', show='host', theme='#7BB0B2',
                perm_capture=False, perm_custom_events=False, perm_aws_data=False):
    '''
    **Description**
        Creates a new team

    **Arguments**
        - **name**: the name of the team to create.
        - **memberships**: dictionary of (user-name, team-role) pairs that should describe new memberships of the team.
        - **filter**: the scope that this team is able to access within Sysdig Monitor.
        - **description**: describes the team that will be created.
        - **show**: possible values are *host*, *container*.
        - **theme**: the color theme that Sysdig Monitor will use when displaying the team.
        - **perm_capture**: if True, this team will be allowed to take sysdig captures.
        - **perm_custom_events**: if True, this team will be allowed to view all custom events from every user and agent.
        - **perm_aws_data**: if True, this team will have access to all AWS metrics and tags, regardless of the team's scope.

    **Success Return Value**
        The newly created team.

    **Example**
        `examples/user_team_mgmt.py <https://github.com/draios/python-sdc-client/blob/master/examples/user_team_mgmt.py>`_
    '''
    reqbody = {
        'name': name,
        'description': description,
        'theme': theme,
        'show': show,
        'canUseSysdigCapture': perm_capture,
        'canUseCustomEvents': perm_custom_events,
        'canUseAwsMetrics': perm_aws_data,
    }

    # Map user-names to IDs
    if memberships != None and len(memberships) != 0:
        res = self._get_user_id_dict(memberships.keys())
        if res[0] == False:
            return [False, 'Could not fetch IDs for user names']
        reqbody['userRoles'] = [
            {
                'userId': user_id,
                'role': memberships[user_name]
            }
            for (user_name, user_id) in res[1].items()
        ]
    else:
        reqbody['users'] = []

    if filter != '':
        reqbody['filter'] = filter

    res = requests.post(self.url + '/api/teams', headers=self.hdrs, data=json.dumps(reqbody), verify=self.ssl_verify)
    if not self._checkResponse(res):
        return [False, self.lasterr]
    return [True, res.json()]


SdMonitorClient.drop_dashboards = drop_dashboards
SdMonitorClient.restore_dashboards_from = restore_dashboards_from
SdMonitorClient.save_dashboards_to = save_dashboards_to
SdMonitorClient.drop_alerts = drop_alerts
SdMonitorClient.restore_alerts_from = restore_alerts_from
SdMonitorClient.save_alerts_to = save_alerts_to
SdMonitorClient.save_notification_channels_to = save_notification_channels_to
SdMonitorClient.drop_notification_channels = drop_notification_channels
SdMonitorClient.restore_notification_channels_from = restore_notification_channels_from
SdMonitorClient.save_users_to = save_users_to
SdMonitorClient.get_all_teams = get_all_teams  # TODO: Remove when pull request is accepted
SdMonitorClient.get_notification_channels = get_notification_channels  # TODO: Remove when pull request is accepted
SdMonitorClient.create_notification_channel = create_notification_channel  # TODO: Remove when pull request is accepted
SdMonitorClient.save_teams_to = save_teams_to
SdMonitorClient.drop_teams = drop_teams
SdMonitorClient.restore_teams_from = restore_teams_from
SdMonitorClient.restore_users_from = restore_users_from
# SdMonitorClient.delete_user = delete_user  # Replacement. Compatible with Python 3. TODO: Remove it when sdcclient becomes fully compatible with Python 3
# SdMonitorClient.create_team = create_team  # Replacement. Compatible with Python 3. TODO: Remove it when sdcclient becomes fully compatible with Python 3

SdSecureClient.drop_policies = drop_policies
SdSecureClient.restore_policies_from = restore_policies_from
SdSecureClient.save_policies_to = save_policies_to
SdSecureClient.save_users_to = save_users_to
SdSecureClient.get_all_teams = get_all_teams  # TODO: Remove when pull request is accepted
SdSecureClient.get_notification_channels = get_notification_channels  # TODO: Remove when pull request is accepted
SdSecureClient.create_notification_channel = create_notification_channel  # TODO: Remove when pull request is accepted
SdSecureClient.save_teams_to = save_teams_to
SdSecureClient.drop_teams = drop_teams
SdSecureClient.restore_teams_from = restore_teams_from
SdSecureClient.restore_users_from = restore_users_from
SdSecureClient.save_user_falco_rules_to = save_user_falco_rules_to
SdSecureClient.restore_user_falco_rules_from = restore_user_falco_rules_from
# SdSecureClient.delete_user = delete_user  # Replacement. Compatible with Python 3. TODO: Remove it when sdcclient becomes fully compatible with Python 3
# SdSecureClient.create_team = create_team  # Replacement. Compatible with Python 3. TODO: Remove it when sdcclient becomes fully compatible with Python 3

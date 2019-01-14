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

# Used for numeric enumeration creation
def __enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


EXIT_CODES = __enum('OK',
                    'ERR_METHOD_NOT_FOUND',

                    'ERR_SAVING_DASHBOARDS',
                    'ERR_SAVING_ALERTS',
                    'ERR_SAVING_USERS',
                    'ERR_SAVING_TEAMS',
                    'ERR_SAVING_POLICIES',
                    'ERR_SAVING_NOTIFICATION_CHANNELS',
                    'ERR_SAVING_FALCO_USER_RULES',

                    'ERR_RESTORING_DASHBOARDS',
                    'ERR_RESTORING_ALERTS',
                    'ERR_RESTORING_USERS',
                    'ERR_RESTORING_TEAMS',
                    'ERR_RESTORING_POLICIES',
                    'ERR_RESTORING_NOTIFICATION_CHANNELS',
                    'ERR_RESTORING_FALCO_USER_RULES',

                    'ERR_CREATING_USER',
                    'ERR_CREATING_DASHBOARD',

                    'ERR_DELETING_USER',
                    'ERR_DELETING_DASHBOARD',
                    'ERR_DELETING_POLICY')

# Specifies where the data must be backed up / restored from
BACKUP_RESTORE_FILES = __enum(DASHBOARDS="dashboards.json",
                              ALERTS="alerts.json",
                              USERS='users.json',
                              TEAMS_MONITOR='teams_monitor.json',
                              POLICIES='policies.json',
                              TEAMS_SECURE='teams_secure.json',
                              NOTIFICATION_CHANNELS='notification_channels.json',
                              USER_FALCO_RULES="user_falco_rules.json")

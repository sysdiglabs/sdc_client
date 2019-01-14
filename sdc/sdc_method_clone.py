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

from sdc.sdc_extend import SdMonitorClient, SdSecureClient
from sdc.sdc_method_backup import backup_monitor, backup_secure
from sdc.sdc_method_restore import restore_monitor, restore_secure
from sdc.sdc_enums import EXIT_CODES, BACKUP_RESTORE_FILES
import tempfile
import os.path


def clone_all_monitor(origin: SdMonitorClient, dest: SdMonitorClient) -> bool:
    with tempfile.TemporaryDirectory() as tmpdir:
        ok, res = origin.save_dashboards_to(os.path.join(tmpdir, BACKUP_RESTORE_FILES.DASHBOARDS))
        if not ok:
            print('Error saving dashboards: ', res)
            return EXIT_CODES.ERR_SAVING_DASHBOARDS

        ok, res = origin.save_alerts_to(os.path.join(tmpdir, BACKUP_RESTORE_FILES.ALERTS))
        if not ok:
            print('Error saving alerts: ', res)
            return EXIT_CODES.ERR_SAVING_ALERTS

        dest.drop_dashboards()
        ok, res = dest.restore_dashboards_from(os.path.join(tmpdir, BACKUP_RESTORE_FILES.DASHBOARDS), fromAllUsers=True)
        if not ok:
            print('Error restoring dashboards: ', res)
            return EXIT_CODES.ERR_RESTORING_DASHBOARDS

        dest.drop_alerts()
        ok, res = dest.restore_alerts_from(os.path.join(tmpdir, BACKUP_RESTORE_FILES.ALERTS),
                                           remove_notification_channels=True)
        if not ok:
            print('Error restoring alerts: ', res)
            return EXIT_CODES.ERR_RESTORING_ALERTS
    return True


def clone_all_secure(origin: SdSecureClient, dest: SdSecureClient) -> bool:
    with tempfile.TemporaryDirectory() as tmpdir:
        if backup_secure(origin, tmpdir) != EXIT_CODES.OK:
            print("Error retrieving data from the origin")
            return False

        if restore_secure(dest, tmpdir) != EXIT_CODES.OK:
            print("Error pushing data to the destination")
            return False
    return True

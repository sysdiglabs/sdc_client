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

from sdc.sdc_enums import EXIT_CODES
from sdc.sdc_extend import SdMonitorClient, SdSecureClient
from sdc.sdc_config import load_config_env
from sdc.sdc_method_restore import restore_monitor, restore_secure
from . import subparser


def restore(args):
    if not os.path.isdir(args.path):
        raise NotADirectoryError(f"{args.path} is not a correct directory")

    config = load_config_env(args.file, args.env)

    if config["token"] is None:
        raise Exception("Token not provided, can't perform restore")

    if config["kind"] == "monitor":
        sdmonitor = SdMonitorClient(config["token"], config["url"])
        if restore_monitor(sdmonitor, args.path, all_users=args.all_users) != EXIT_CODES.OK:
            print("There has been an error restoring Monitor")
        return

    if config["kind"] == "secure":
        sdsecure = SdSecureClient(config["token"], config["url"])
        if restore_secure(sdsecure, args.path) != EXIT_CODES.OK:
            print("There has been an error restoring Secure")
        return

    raise Exception(f"Unknown kind {config['kind']}")


_restoreParser = subparser.add_parser("restore",
                                      description="Restores all the information dumped from 'backup' to Monitor and "
                                                  "Secure.")
_restoreParser.add_argument("path", help="Directory where the data must be restored from.")
_restoreParser.add_argument("--all-users", dest="all_users", default=False, action='store_true',
                            help="Restore dashboards even if you are not the owner "
                                 "(may duplicate the dashboards if they already exist in the environment)")
_restoreParser.set_defaults(func=restore)

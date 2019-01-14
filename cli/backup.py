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

from sdc.sdc_config import load_config_env
from sdc.sdc_enums import EXIT_CODES
from sdc.sdc_extend import SdMonitorClient, SdSecureClient
from sdc.sdc_method_backup import backup_monitor, backup_secure
import os.path
from . import subparser


def backup(args):
    if not os.path.isdir(args.path):
        raise NotADirectoryError(f"{args.path} is not a correct directory")

    config = load_config_env(args.file, args.env)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, can't perform Backup")

    if config["kind"] == "monitor":
        sdmonitor = SdMonitorClient(config["token"], config["url"])
        if backup_monitor(sdmonitor, args.path) != EXIT_CODES.OK:
            print("There has been an error creating the Monitor backup")
        return

    if config["kind"] == "secure":
        sdsecure = SdSecureClient(config["token"], config["url"])
        if backup_secure(sdsecure, args.path) != EXIT_CODES.OK:
            print("There has been an error creating the Secure backup")
        return

    raise Exception(f"Unknown kind {config['kind']}")


_backupParser = subparser.add_parser("backup",
                                     description="Dumps all the information from Monitor and Secure to a directory.")
_backupParser.add_argument("path", help="Directory where the data must be saved to.")
_backupParser.set_defaults(func=backup)

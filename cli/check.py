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
from sdc.sdc_config import load_config_env
from sdc.sdc_extend import SdMonitorClient, SdSecureClient
from sdc.sdc_method_check import check_monitor, check_secure
from . import subparser


def check(args):
    if not os.path.isdir(args.path):
        raise NotADirectoryError(f"{args.path} is not a correct directory")

    print("Checking if there are remote changes...")

    config = load_config_env(args.file, args.env)
    token = config["token"]
    kind = config["kind"]
    url = config["url"]

    if token is None or token == "":
        raise Exception("Token not provided, can't perform check")

    if kind == "monitor":
        something_changed = check_monitor(SdMonitorClient(token, url), args.path)
        exit(0 if not something_changed else 1)

    if kind == "secure":
        something_changed = check_secure(SdSecureClient(token, url), args.path)
        exit(0 if not something_changed else 1)

    print(f"unknown kind of remote environment: {kind}")
    exit(2)


_check_parser = subparser.add_parser("check", description="Checks if something has changed in the remote environment "
                                                          "comparing it with the backed up version")
_check_parser.add_argument("path", help="Path of the backup.")
_check_parser.set_defaults(func=check)

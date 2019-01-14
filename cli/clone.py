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
from sdc.sdc_extend import SdMonitorClient, SdSecureClient
from sdc.sdc_method_clone import clone_all_monitor, clone_all_secure
from . import subparser


def clone(args):
    config = load_config_env(args.file, args.env)
    target = load_config_env(args.file, args.target)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, cannot retrieve information from the origin to clone")

    if target["token"] is None or target["token"] == "":
        raise Exception("Token not provided, cannot retrieve information of the destination to override")

    if config["kind"] != target["kind"]:
        raise Exception("Origin and destination env types are not compatible")

    if config["kind"] == "monitor":
        origin = SdMonitorClient(config["token"], config["url"])
        destination = SdMonitorClient(target["token"], target["url"])
        ok = clone_all_monitor(origin, destination)
        if ok:
            print("Clone complete")

    if config["kind"] == "secure":
        origin = SdSecureClient(config["token"], config["url"])
        origin = SdSecureClient(target["token"], target["url"])
        ok = clone_all_secure(origin, destination)


__clone_parser = subparser.add_parser("clone",
                                      description="Clones all the selected environment information to another one")
__clone_parser.add_argument("-t", dest="target", required=True, help="Target environment")
__clone_parser.set_defaults(func=clone)

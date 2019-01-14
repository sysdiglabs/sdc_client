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
from sdc.sdc_method_show import show_users, show_dashboards, show_policies
from sdc.sdc_extend import SdMonitorClient, SdSecureClient
from . import subparser


def show(args):
    _show_parser.print_help()
    exit(1)


def user(args):
    config = load_config_env(args.file, args.env)
    if config["token"] is None or config["token"] == "":
        raise Exception("Token was not provided")
    sdmonitor = SdMonitorClient(config["token"], config["url"])
    show_users(sdmonitor)


def dashboard(args):
    config = load_config_env(args.file, args.env)
    if config["token"] is None or config["token"] == "":
        raise Exception("Token was not provided")
    sdmonitor = SdMonitorClient(config["token"], config["url"])
    show_dashboards(sdmonitor)

def policy(args):
    config = load_config_env(args.file, args.env)
    if config["token"] is None or config["token"] == "":
        raise Exception("Token was not provided")
    if config["kind"] != "secure":
        raise Exception("Selected environment is not Sysdig Secure")

    sdsecure = SdSecureClient(config["token"], config["url"])
    show_policies(sdsecure)


_show_parser = subparser.add_parser("show", description="Shows information about Sysdig.")
_show_subparser = _show_parser.add_subparsers(dest="show")
_show_parser.set_defaults(func=show)

_user_parser = _show_subparser.add_parser("users", description="Lists all users from Sysdig Monitor.")
_user_parser.set_defaults(func=user)

_dashboards_parser = _show_subparser.add_parser("dashboards", description="List all dashboards from Sysdig Monitor.")
_dashboards_parser.set_defaults(func=dashboard)

_policies_parser = _show_subparser.add_parser("policies", description="List all policies from Sysdig Secure.")
_policies_parser.set_defaults(func=policy)
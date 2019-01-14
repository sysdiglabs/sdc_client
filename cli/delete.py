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
from . import subparser

from sdc.sdc_extend import SdMonitorClient, SdSecureClient
from sdc.sdc_method_delete import delete_user, delete_dashboards, delete_policies


def delete(_):
    _delete_parser.print_help()
    exit(1)


def user(args):
    config = load_config_env(args.file, args.env)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, cannot delete a user")

    sdmonitor = SdMonitorClient(config["token"], config["url"])
    res = delete_user(sdmonitor, email=args.email)
    if res == EXIT_CODES.OK:
        print(f"Deleted user {args.email}")


def dashboards(args):
    config = load_config_env(args.file, args.env)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, cannot delete a dashboard")

    if config["kind"] != "monitor":
        raise Exception("Selected environment is not Sysdig Monitor")

    sdmonitor = SdMonitorClient(config["token"], config["url"])
    res = delete_dashboards(sdmonitor, ids=args.ids)
    if res == EXIT_CODES.OK:
        print(f"Deleted dashboards: {args.ids}")

def policies(args):
    config = load_config_env(args.file, args.env)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, cannot delete policies")

    if config["kind"] != "secure":
        raise Exception("Selected environment is not Sysdig Secure")

    sdsecure = SdSecureClient(config["token"], config["url"])
    res = delete_policies(sdsecure, ids=args.ids)
    if res == EXIT_CODES.OK:
        print(f"Deleted policies: {args.ids}")


_delete_parser = subparser.add_parser("delete", description="Deletes users, teams, groups, etc. ")
_delete_subparser = _delete_parser.add_subparsers(dest="delete")
_delete_parser.set_defaults(func=delete)

# Users
_user_parser = _delete_subparser.add_parser("user",
                                            description="Remove an user from Sysdig Monitor")
_user_parser.add_argument("email", help="The email address of the user that will be removed from Sysdig Monitor"),
_user_parser.set_defaults(func=user)

# Dashboards
_dashboard_parser = _delete_subparser.add_parser("dashboards", description="Removes a dashboard from Sysdig Monitor")
_dashboard_parser.add_argument("ids", metavar="ID", nargs="+",
                               help="The IDs of the dashboards that will be removed from Sysdig Monitor")
_dashboard_parser.set_defaults(func=dashboards)

# Policies
_policy_parser = _delete_subparser.add_parser("policies", description="Removes policies from Sysdig Secure")
_policy_parser.add_argument("ids", metavar="ID", nargs="+",
                            help="The IDs of the policies that will be removed from Sysdig Secure")
_policy_parser.set_defaults(func=policies)
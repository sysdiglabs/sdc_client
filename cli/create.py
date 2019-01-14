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
from sdc.sdc_extend import SdMonitorClient
from sdc.sdc_method_create import create_user, create_dashboards_from_file
from . import subparser
import os.path


def create(args):
    _create_parser.print_help()
    exit(1)


def user(args):
    config = load_config_env(args.file, args.env)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, cannot create a user")

    sdmonitor = SdMonitorClient(config["token"], config["url"])
    res = create_user(sdmonitor, email=args.email, first_name=args.first_name, last_name=args.last_name,
                      system_role=args.system_role)
    if res == EXIT_CODES.OK:
        print(f"Created user {args.email}")
    else:
        print(f"There has been an error creating the user")

def dashboards(args):
    config = load_config_env(args.file, args.env)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, cannot create a user")

    sdmonitor = SdMonitorClient(config["token"], config["url"])

    if not os.path.isfile(args.input_file):
        raise Exception(f"File {args.input_file} does not exist or is not a file.")

    with open(args.input_file, "r") as file:
        res = create_dashboards_from_file(sdmonitor, file)
        if res == EXIT_CODES.OK:
            print("Dashboards created")
        else:
            print("Error creating dashboards")

_create_parser = subparser.add_parser("create", description="Creates users, teams, groups, etc. ")
_create_subparser = _create_parser.add_subparsers(dest="create")
_create_parser.set_defaults(func=create)

# User
_user_parser = _create_subparser.add_parser("user", description="Creates an invitation to the user with desired "
                                                                "information")
_user_parser.add_argument("email", help="The email address of the user that will be invited to use Sysdig Monitor"),
_user_parser.add_argument("first_name", help="The first name of the user being invited"),
_user_parser.add_argument("last_name", help="The last name of the user being invited"),
_user_parser.add_argument("system_role", default="ROLE_USER", nargs="?",
                          help="System-wide privilege level for this user regardless of team. specify 'ROLE_CUSTOMER' "
                               "to create an Admin. If not specified, default is a non-Admin ('ROLE_USER').")
_user_parser.set_defaults(func=user)

# Dashboards
_dashboard_parser = _create_subparser.add_parser("dashboards", description="Creates dashboards in Sysdig Monitor")
_dashboard_parser.add_argument("-i", dest="input_file", required=True,
                               help="Input file with all the dashboards information as retrieved by the 'get' method")
_dashboard_parser.set_defaults(func=dashboards)

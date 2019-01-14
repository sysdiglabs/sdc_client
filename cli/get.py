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
from sdc.sdc_extend import SdMonitorClient
from sdc.sdc_method_get import get_dashboards
from . import subparser


def get(args):
    _get_parser.print_help()
    exit(1)


def dashboards(args):
    config = load_config_env(args.file, args.env)

    if config["token"] is None or config["token"] == "":
        raise Exception("Token not provided, cannot retrieve dashboards")

    sdmonitor = SdMonitorClient(config["token"], config["url"])
    get_dashboards(sdmonitor, args.ids, args.format)


_get_parser = subparser.add_parser("get", description="Retrieves an object from the API in JSON format")
_get_subparser = _get_parser.add_subparsers(dest="get")
_get_parser.set_defaults(func=get)

_dashboard_parser = _get_subparser.add_parser("dashboards",
                                              description="Retrieves dashboards information")
_dashboard_parser.add_argument("ids", metavar="ID", help="The ID of the dashboards to retrieve", nargs="+"),
_dashboard_parser.add_argument("-o", dest="format", help="Output format", choices=["yaml", "json"], default="json")
_dashboard_parser.set_defaults(func=dashboards)

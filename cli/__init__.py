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

from argparse import ArgumentParser

cli = ArgumentParser()
subparser = cli.add_subparsers(dest="subcommand")

# Global arguments
cli.add_argument("-e", "--env", help="Uses a preconfigured environment in the config file. If it's not provided, the "
                                     "environment will be retrieved by the env var SDC_ENV. Also, if this env var "
                                     "is not provided, the token will be retrieved from the env var SDC_TOKEN "
                                     "as a fallback, and it will use app.sysdigcloud.com as the url.")
cli.add_argument("-f", dest="file",
                 help="Uses the provided file as a config file. If the config file is not provided, it will be "
                      "searched at ~/.config/sdc_client/config.yml, /etc/sdc_client/config.yml and /sdc_client.yml.")

from . import backup, restore, create, delete, show, check, get, clone

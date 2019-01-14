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
import os.path
import yaml

__default_config_paths = [f"{os.environ.get('HOME')}/.config/sdc_client/config.yml", "/etc/sdc_client/config.yml",
                          "/sdc_client.yml"]
__default_configs = {
    "kind": "monitor",
    "token": os.environ.get('SDC_TOKEN'),
    "url": 'https://app.sysdigcloud.com',
}


# Configuration file must have the following structure
# envs:
#   envName1:
#     kind: "monitor"
#     token: "<your token>"
#     url: "<your url>"
#   envName2:
#     kind: "secure"
#     token: "<your token>"
#     url: "<your url>"
def load_config_env(path=None, env=None):
    if env is None or env == "":
        env = os.getenv("SDC_ENV", None)
        if env is None:
            return __config_with_defaults()

    if path is None or path == "":
        found = False
        for file_path in __default_config_paths:
            if os.path.isfile(file_path):
                path = file_path
                found = True
        if not found:
            raise FileNotFoundError("couldn't find a default config file")
    else:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"couldn't find the provided config file: {path}")

    try:
        with open(path, "r") as f:
            config = yaml.load(f)
            if "envs" not in config:
                raise Exception("config file does not have a envs parent")

            if env not in config["envs"]:
                raise Exception(f"environment provided '{env}' not found in the configuration file, "
                                f"envs found: {list(config['envs'].keys())}")

            return __config_with_defaults(config["envs"][env])

    except yaml.YAMLError as exc:
        raise Exception("error in configuration file:", exc)


def __config_with_defaults(config=None):
    if config is None:
        return __default_configs

    for key in __default_configs.keys():
        if key not in config or config[key] is None or config[key] == "":
            config[key] = __default_configs[key]

    if "url" in config:
        config["url"] = config["url"].strip("/")

    return config

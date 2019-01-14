Sysdig Monitor/Secure Python CLI Client
=======================================

A CLI client that allows you to perform API calls to Sysdig Monitor/Sysdig Secure.

Installation
------------

#### Install requirements

```bash
pip install -r requirements.txt
```

Quick start
-----------

_Note:_ in order to use this client you must first obtain a Sysdig Monitor/Secure API token.

You can get your user's token in the _Sysdig Monitor API_ section of the settings page for 
[monitor](https://app.sysdigcloud.com/#/settings/user) or [secure](https://secure.sysdig.com/#/settings/user) and 
setup config file.
It can be set up in the following paths:

- Per user: `$HOME/.config/sdc_client/config.yml`
- As system config: `/etc/sdc_client/config.yml`
- Recommended for containers: `/sdc_client.yml`
``
You can also use the `-f FILE` parameter to specify where's the config file. 

The config file has the following structure:

```yaml
envs:
  envName1:
    kind: "monitor"
    token: "<your token>"
    url: "<your url>"
  envName2:
    kind: "secure"
    token: "<your token>"
    url: "<your url>"
  ...
```

You can use the `-e ENV` parameter or the env var `SDC_ENV` to specify what environment you want to use.
If you don't provide the environment, the client will fall back to the `SDC_TOKEN` env var.

#### Backup all data

```bash
./sdc_client -e <envName> backup <output_folder>
```

#### Restore all data

```bash
./sdc_client -e <envName> restore <input_folder>
```

The input folder should be the same used for the backup. All data will be dropped (except users) 
and restored from the backup.

#### List all users

```bash
./sdc_client -e <envName> show users
```

#### Create a user

```bash
./sdc_client -e <envName> create user <user_email> <first_name> <last_name> <system_role>
```

#### Delete a user 

```bash
./sdc_client -e <envName> delete user <user_email>
``` 


#### List all dashboards

```bash
./sdc_client -e <envName> show dashboards
```

#### Retrieve some dashboards

```bash
./sdc_client -e <envName> get dashboards <ID> <[ID...]> [-o yaml]
```

#### Create some dashboards from retrieved ones

```bash
./sdc_client -e <envName> create dashboards -i <input_file>
```

#### Delete some dashboards

```bash
./sdc_client -e <envName> delete dashboards <ID> <[ID...]>
```

#### Clone one dashboards and alerts from one environment to another one

```bash
./sdc_client -e <origin> clone -t <target_destination>
```

TODO List
---------

- Complete API Support

License
-------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

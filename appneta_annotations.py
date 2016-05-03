#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ansible module to add appneta annotations.

(c) 2015, Niranjan Bommu <niranjan.bommu@gmail.com>

This file is part of Ansible

Ansible is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Ansible is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
"""
DOCUMENTATION = '''

module: appneta_annotations
version_added: "1.0"
author: Niranjan Bommu
short_description: Notify appneta about app deployments
description:
   - Notify appneta about app deployments (see http://http://dev.appneta.com/docs/api-v2/annotations.html)
options:
  key:
    description:
      - API key.
    required: true
  appname:
    description:
      - Name of the application
    required: false
  message:
    description:
      - Text annotation for the deployment
    required: true
  username:
     description:
       - user name
  hostname:
    description:
      - The hostname for this deployment
    required: false

# informational: requirements for nodes
requirements: [ urllib, urllib2 ]
'''

EXAMPLES = '''
- appneta_deployment: key=AAAAAA
                      message='message'
                      appname=myapp
                      hostname='hostname'
                      username='username'
'''

import json
from urllib import urlencode
from urllib2 import urlopen, URLError

# ===========================================
# Module execution.
#

def main():

    module = AnsibleModule(
        argument_spec=dict(
            key=dict(required=True),
            message=dict(required=True),
            appname=dict(required=False),
            hostname=dict(required=False),
            username=dict(required=False),
        ),
        supports_check_mode=True
    )

    # build list of params
    params = {}
    if module.params["appname"]:
        params["appname"] = module.params["appname"]
    else:
        module.fail_json(msg="you must set 'appname'")

    for item in [ "key", "message", "appname", "username", "hostname"]:
        if module.params[item]:
            params[item] = module.params[item]

    # If we're in check mode, just exit pretending like we succeeded
    if module.check_mode:
        module.exit_json(changed=True)

    # Send the data to appneta
    try:
       req = urlopen("https://api.tv.appneta.com/api-v2/log_message", urlencode(params))
       module.exit_json(changed=True)
    except URLError, e:
        module.fail_json(msg="Error sending log message: " + str(e))

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()

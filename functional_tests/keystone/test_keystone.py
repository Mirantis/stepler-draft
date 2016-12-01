"""
--------------
Keystone tests
--------------
"""

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pytest

from stepler import config
from stepler.third_party import utils


@pytest.mark.idempotent_id('76f823ac-5c8b-4617-a4cc-9e30257a679f')
def test_restart_all_services(cirros_image,
                              tiny_flavor,
                              keypair,
                              net_subnet_router,
                              security_group,
                              create_user,
                              user_steps,
                              os_faults_steps,
                              server_steps):
    """**Scenario:** Check that keystone works after restarting services.

    **Setup:**

    #. Create cirros image
    #. Create tiny flavor
    #. Create key pair
    #. Create network with subnet and router

    **Steps:**

    #. Create new user 1
    #. Check that user 1 is present in user list
    #. Restart keystone services
    #. Check that user 1 is present in user list
    #. Create new user 2
    #. Check that user 2 is present in user list
    #. Create VM
    #. Check its status = ACTIVE

    **Teardown:**

    #. Delete VM
    #. Delete network, subnet, router
    #. Delete users 1 and 2
    #. Delete key pair
    #. Delete tiny flavor
    #. Delete cirros image
    """
    user_name = next(utils.generate_ids('user'))
    user1 = create_user(user_name=user_name, password=user_name)

    os_faults_steps.restart_services([config.KEYSTONE])

    user_steps.check_user_presence(user1)
    user_name = next(utils.generate_ids('user'))
    create_user(user_name=user_name, password=user_name)

    network, _, _ = net_subnet_router
    server_steps.create_servers(image=cirros_image,
                                flavor=tiny_flavor,
                                networks=[network],
                                keypair=keypair,
                                security_groups=[security_group])

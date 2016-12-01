"""
---------------------
Server metadata tests
---------------------
"""

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest

from stepler import config
from stepler.third_party import utils

TEST_METADATA_INFO = {'key': next(utils.generate_ids('test_meta'))}

SET_META_CMD_TEMPLATE = (
    '{openrc_cmd}; nova host-meta {host} set {key}={value}'.format(
        openrc_cmd=config.OPENRC_ACTIVATE_CMD,
        host='{host}',
        key=TEST_METADATA_INFO.keys()[0],
        value=TEST_METADATA_INFO.values()[0]))
DEL_META_CMD_TEMPLATE = (
    '{openrc_cmd}; nova host-meta {host} delete {key}'.format(
        openrc_cmd=config.OPENRC_ACTIVATE_CMD,
        host='{host}',
        key=TEST_METADATA_INFO.keys()[0]))


# TODO(akoryagin) need to add check that we have 2 or more computes
@pytest.mark.idempotent_id('2af40022-a2ca-4615-aff3-2c07354ce983')
def test_put_metadata_on_instances_on_single_compute(
        security_group,
        ubuntu_image,
        keypair,
        network,
        subnet,
        nova_availability_zone_hosts,
        flavor_steps,
        server_steps,
        os_faults_steps,
        execute_command_with_rollback):
    """**Scenario:** Put metadata on all instances scheduled on a single
    compute node.

    **Setup:**

    #. Create security group
    #. Get Glance ubuntu image OR download and create it if ubuntu image is
        not present.
    #. Create keypair
    #. Create network and subnetwork

    **Steps:**

    #. Get flavor ``m1.small``
    #. Get FQDNs of nova hosts
    #. Create 2 nova servers on host 1
    #. Create 2 nova servers on host 2
    #. From controller node add new 'key=value' to metadata of servers,
        located on host 1.
    #. Check that servers from host 1 have 'key=value' in their metadata
    #. Check that servers from host 2 do NOT have 'key=value' in their metadata
    #. From controller node delete 'key=value' from metadata of servers,
        located on host 1.
    #. Check that servers from host 1 and host 2 do NOT have 'key=value' in
        their metadata

    **Teardown:**

    #. Delete servers
    #. Delete keypair
    #. Delete security group
    #. Delete network and subnetwork
    """
    flavor = flavor_steps.get_flavor(name=config.FLAVOR_SMALL)
    host_1 = nova_availability_zone_hosts[0]
    host_2 = nova_availability_zone_hosts[1]

    controller_node = os_faults_steps.get_node(service_names=[config.NOVA_API])

    cmd_set_meta = SET_META_CMD_TEMPLATE.format(host=host_1)
    cmd_del_meta = DEL_META_CMD_TEMPLATE.format(host=host_1)

    host1_servers = server_steps.create_servers(
        count=2,
        image=ubuntu_image,
        flavor=flavor,
        networks=[network],
        keypair=keypair,
        security_groups=[security_group],
        availability_zone='nova:{}'.format(host_1))

    host2_servers = server_steps.create_servers(
        count=2,
        image=ubuntu_image,
        flavor=flavor,
        networks=[network],
        keypair=keypair,
        security_groups=[security_group],
        availability_zone='nova:{}'.format(host_2))

    with execute_command_with_rollback(
            nodes=controller_node,
            cmd=cmd_set_meta,
            rollback_cmd=cmd_del_meta):

        for server in host1_servers:
            server_steps.check_metadata_presence(
                server, TEST_METADATA_INFO,
                timeout=config.SERVER_UPDATE_TIMEOUT)

        for server in host2_servers:
            server_steps.check_metadata_presence(
                server, TEST_METADATA_INFO, present=False,
                timeout=config.SERVER_UPDATE_TIMEOUT)

    for server in host1_servers + host2_servers:
        server_steps.check_metadata_presence(
            server, TEST_METADATA_INFO, present=False,
            timeout=config.SERVER_UPDATE_TIMEOUT)

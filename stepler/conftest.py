"""
---------------
Global conftest
---------------

Includes fixtures available in global scope among all tests.
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from stepler.cinder.conftest import *  # noqa
from stepler.fixtures import *  # noqa
from stepler.glance.conftest import *  # noqa
from stepler.heat.conftest import *  # noqa
from stepler.keystone.conftest import *  # noqa
from stepler.neutron.conftest import *  # noqa
from stepler.nova.conftest import *  # noqa
from stepler.os_faults.conftest import *  # noqa

__all__ = sorted([  # sort for documentation
    'admin_ssh_key_path',
    'auth_url',
    'ip_by_host',
    'get_session',
    'session',
    'skip_test',
    'uncleanable',
    'report_log',
    'report_dir',

    'get_backup_steps',
    'backup_steps',
    'create_backup',
    'cleanup_backups',
    'cinder_client',
    'get_cinder_client',
    'cinder_quota_steps',
    'big_snapshot_quota',
    'volume_size_quota',
    'get_snapshot_steps',
    'snapshot_steps',
    'cleanup_snapshots',
    'volume_snapshot',
    'transfer_steps',
    'create_volume_transfer',
    'get_transfer_steps',
    'cleanup_transfers',
    'volume_type_steps',
    'create_volume_type',
    'volume_type',
    'cleanup_volumes',
    'get_volume_steps',
    'primary_volumes',
    'unexpected_volumes_cleanup',
    'upload_volume_to_image',
    'volume',
    'volume_steps',

    'heat_client',
    'stack_steps',
    'create_stack',
    'empty_stack',
    'read_heat_template',
    'heat_resource_steps',
    'heat_resource_type_steps',
    'get_template_path',

    'get_glance_client',
    'glance_client_v1',
    'glance_client_v2',
    'cirros_image',
    'get_glance_steps',
    'glance_steps',
    'glance_steps_v1',
    'glance_steps_v2',
    'ubuntu_image',
    'ubuntu_xenial_image',

    'create_group',
    'create_domain',
    'domain_steps',
    'domain',
    'group_steps',
    'keystone_client',
    'create_project',
    'project_steps',
    'project',
    'current_project',
    'admin_role',
    'create_role',
    'role_steps',
    'role',
    'admin',
    'create_user',
    'user_steps',
    'user',
    'new_user_with_project',

    'create_network',
    'network',
    'public_network',
    'create_port',
    'port',
    'create_subnet',
    'subnet',
    'create_router',
    'router',
    'add_router_interfaces',
    'create_port',
    'port_steps',
    'neutron_client',
    'get_neutron_client',
    'network_steps',
    'get_network_steps',
    'router_steps',
    'get_router_steps',
    'subnet_steps',
    'get_subnet_steps',
    'net_subnet_router',
    'neutron_2_networks',
    'neutron_2_servers_different_networks',
    'neutron_2_servers_diff_nets_with_floating',
    'neutron_2_servers_same_network',
    'neutron_2_servers_iperf_different_networks',
    'get_agent_steps',
    'agent_steps',
    'reschedule_router_active_l3_agent',
    'get_neutron_quota_steps',
    'neutron_quota_steps',
    'change_neutron_quota',

    'get_availability_zone_steps',
    'availability_zone_steps',
    'nova_availability_zone',
    'nova_availability_zone_hosts',

    'create_flavor',
    'flavor',
    'flavor_steps',
    'tiny_flavor',

    'nova_create_floating_ip',
    'nova_floating_ip',
    'nova_floating_ip_steps',

    'host_steps',

    'hypervisor_steps',
    'sorted_hypervisors',

    'keypair',
    'keypair_steps',
    'keypairs_cleanup',

    'get_nova_client',
    'nova_client',
    'disable_nova_config_drive',
    'skip_live_migration_tests',
    'unlimited_live_migrations',
    'nova_ceph_enabled',

    'create_security_group',
    'security_group',
    'security_group_steps',

    'nova_volume_steps',
    'attach_volume_to_server',
    'detach_volume_from_server',

    'create_server_context',
    'create_servers_context',
    'get_server_steps',
    'get_ssh_proxy_cmd',
    'server',
    'server_steps',
    'live_migration_server',
    'live_migration_servers',
    'live_migration_servers_with_volumes',
    'servers_cleanup',
    'generate_traffic',
    'unexpected_servers_cleanup',

    'os_faults_client',
    'os_faults_steps',
    'patch_ini_file_and_restart_services',
    'execute_command_with_rollback',
    'nova_api_node',
])

_plugins = [
    'bugs_file',
    'destructive_dispatcher',
    'idempotent_id',
    'reports_cleaner',
    'steps_checker',
]

pytest_plugins = map(lambda plugin: 'stepler.third_party.' + plugin, _plugins)

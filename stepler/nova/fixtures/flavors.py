"""
---------------
Flavor fixtures
---------------
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

import pytest

from stepler import config
from stepler.nova.steps import FlavorSteps
from stepler.third_party.utils import generate_ids

__all__ = [
    'create_flavor',
    'flavor',
    'flavor_steps',
    'tiny_flavor',
]


@pytest.fixture
def flavor_steps(nova_client):
    """Callable function fixture to get nova flavor steps.

    Args:
        nova_client (function): function to get nova client

    Returns:
        function: function to instantiated flavor steps
    """
    return FlavorSteps(nova_client.flavors)


@pytest.yield_fixture
def create_flavor(flavor_steps):
    """Callable function fixture to create nova flavor with options.

    Can be called several times during a test.
    After the test it destroys all created nodes.

    Args:
        flavor_steps (object): instantiated flavor steps

    Returns:
        function: function to create flavors as batch with options
    """
    flavors = []

    def _create_flavor(flavor_name, *args, **kwargs):
        flavor = flavor_steps.create_flavor(flavor_name, *args, **kwargs)
        flavors.append(flavor)
        return flavor

    yield _create_flavor

    for flavor in flavors:
        flavor_steps.delete_flavor(flavor)


@pytest.fixture
def flavor(request, create_flavor):
    """Callable function fixture to create single ova flavor with options.

    Can be called several times during a test.
    After the test it destroys all created nodes.

    Can be parametrized with dict of create_flavor arguments.


    Example:
        @pytest.mark.parametrize('flavor', [
            dict(ram=2048, vcpus=2),
            dict(ram=512, disk=1),
        ], indirect=['flavor'])
        def test_foo(instance):
            # Instance will created with different flavors

    Args:
        request (obj): py.test SubRequest
        create_flavor (function): function to create flavor with options

    Returns:
        function: function to create single flavor with options
    """
    flavor_params = dict(ram=1024, vcpus=1, disk=5)
    flavor_params.update(getattr(request, 'param', {}))
    flavor_name = next(generate_ids('flavor'))
    return create_flavor(flavor_name, **flavor_params)


@pytest.fixture
def tiny_flavor(flavor_steps):
    """Function fixture to find tiny flavor before test.

    Args:
        flavor_steps (object): instantiated flavor steps

    Returns:
        object: tiny flavor
    """
    return flavor_steps.get_flavor(name=config.FLAVOR_TINY)

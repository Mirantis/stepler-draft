"""
---------------
Client fixtures
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

from glanceclient.v1 import client as client_v1
from glanceclient.v2 import client as client_v2
import pytest

__all__ = [
    'get_glance_client',
    'glance_client_v1',
    'glance_client_v2',
]


@pytest.fixture(scope='session')
def get_glance_client(get_session):
    """Callable session fixture to get glance client v1.

    Args:
        get_session (function): function to get keystone session

    Returns:
        function: function to get glance client v1
    """
    def _get_glance_client(version):
        if version == '1':
            return client_v1.Client(session=get_session())

        if version == '2':
            return client_v2.Client(session=get_session())

        raise ValueError("Unexpected glance version: {!r}".format(version))

    return _get_glance_client


@pytest.fixture
def glance_client_v1(get_glance_client):
    """Function fixture to get glance client v1.

    Args:
        get_glance_client (function): function to get glance client

    Returns:
        glanceclient.v1.client.Client: instantiated glance client
    """
    return get_glance_client(version='1')


@pytest.fixture
def glance_client_v2(get_glance_client):
    """Function fixture to get glance client v2.

    Args:
        get_glance_client (function): function to get glance client

    Returns:
        glanceclient.v2.client.Client: instantiated glance client
    """
    return get_glance_client(version='2')

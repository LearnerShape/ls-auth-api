# Copyright (C) 2022  Learnershape and contributors

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from collections import namedtuple
from datetime import datetime
import pdb
import pytest


from ls_auth_api import create_app

access_id, secret_key = "a", "b"


@pytest.fixture(scope="session")
def api_client():
    app = create_app()
    app.config["API_ACCESS_ID"], app.config["API_SECRET_KEY"] = access_id, secret_key
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def api_keys():
    auth = namedtuple("auth", ["access", "secret"])
    yield auth(access_id, secret_key)


@pytest.fixture(scope="module")
def api_users(api_client, api_keys):
    name = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    user = {"name": f"user_{name}_1", "email": f"user_{name}_1@test.com"}
    response = api_client.post(
        f"/api/v1/users/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
        json=user,
    )
    assert response.status_code == 200
    user1 = response.json
    user = {"name": f"user_{name}_2", "email": f"user_{name}_2@test.com"}
    response = api_client.post(
        f"/api/v1/users/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
        json=user,
    )
    assert response.status_code == 200
    user2 = response.json
    return (user1, user2)

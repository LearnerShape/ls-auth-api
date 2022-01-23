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

import pdb
from datetime import datetime


def test_users_get_secure(api_client):
    response = api_client.get(
        f"/api/v1/users/",
    )
    assert response.status_code == 403
    assert response.json["status_code"] == 403


def test_users_get(api_client, api_keys):
    response = api_client.get(
        f"/api/v1/users/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
    )
    assert response.status_code == 200
    assert "users" in response.json.keys()


def test_users_post(api_client, api_keys):
    user = {"name": "test_users_post", "email": "test_users_post@test.com"}
    response = api_client.post(
        f"/api/v1/users/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
        json=user,
    )
    assert response.status_code == 200
    for i in ["id", "name", "email"]:
        assert i in response.json.keys()

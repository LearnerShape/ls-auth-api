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


def test_skills_get_secure(api_client, api_users):
    api_user1, api_user2 = api_users
    response = api_client.get(
        f"/api/v1/users/{api_user1['id']}/skills/",
    )
    assert response.status_code == 403
    assert response.json["status_code"] == 403


def test_skills_get(api_client, api_keys, api_users):
    api_user1, api_user2 = api_users
    response = api_client.get(
        f"/api/v1/users/{api_user1['id']}/skills/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
    )
    assert response.status_code == 200
    assert "skills" in response.json.keys()


def test_skills_post(api_client, api_keys, api_users):
    api_user1, api_user2 = api_users
    skill = {
        "author_id": api_user1["id"],
        "skill_type": "skill A",
        "skill_details": {"name": "test", "subject": "testing"},
    }
    response = api_client.post(
        f"/api/v1/users/{api_user1['id']}/skills/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
        json=skill,
    )
    assert response.status_code == 200
    for i in [
        "id",
        "author_id",
        "skill_type",
        "skill_details",
    ]:
        assert i in response.json.keys()

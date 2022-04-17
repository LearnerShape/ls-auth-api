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


def test_credentials_get_secure(api_client, api_users):
    api_user1, api_user2 = api_users
    response = api_client.get(
        f"/api/v1/users/{api_user1['id']}/credentials/",
    )
    assert response.status_code == 403
    assert response.json["status_code"] == 403


def test_credentials_get(api_client, api_keys, api_users):
    api_user1, api_user2 = api_users
    response = api_client.get(
        f"/api/v1/users/{api_user1['id']}/credentials/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
    )
    assert response.status_code == 200
    assert "credentials" in response.json.keys()


def create_credential(api_client, api_keys, user_id, credential):
    response = api_client.post(
        f"/api/v1/users/{user_id}/credentials/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
        json=credential,
    )
    return response


def test_credentials_post_self(api_client, api_keys, api_users, skills):
    """Test creating a new credential"""
    api_user1, api_user2 = api_users
    credential = {
        "holder": api_user1["id"],
        "skill": skills[api_user1["id"]][0]["id"],
        "issuer": api_user1["id"],
        "status": "Requested",
    }
    user_id = api_user1["id"]
    response = create_credential(api_client, api_keys, user_id, credential)

    assert response.status_code == 200
    for i in ["id", "holder", "skill", "issuer", "status"]:
        assert i in response.json.keys()


def test_credentials_post_other(api_client, api_keys, api_users, skills):
    """Test creating a new credential"""
    api_user1, api_user2 = api_users
    credential = {
        "holder": api_user1["id"],
        "skill": skills[api_user1["id"]][0]["id"],
        "issuer": api_user2["id"],
        "status": "Requested",
    }
    user_id = api_user2["id"]
    response = create_credential(api_client, api_keys, user_id, credential)

    assert response.status_code == 200
    for i in ["id", "holder", "skill", "issuer", "status"]:
        assert i in response.json.keys()


def test_credentials_post_status(api_client, api_keys, api_users, skills):
    """Test that the issuer matches the user id provided in the URI if
    status other than Requested"""
    api_user1, api_user2 = api_users
    credential = {
        "holder": api_user1["id"],
        "skill": skills[api_user1["id"]][0]["id"],
        "issuer": api_user2["id"],
        "status": "Issued",
    }
    user_id = api_user1["id"]  # This is different to the issue ID - so expect error
    response = create_credential(api_client, api_keys, user_id, credential)
    assert response.status_code == 403


def update_credential_status(api_client, api_keys, user_id, credential_id, status):
    cred_update = {"status": status}
    response = api_client.patch(
        f"/api/v1/users/{user_id}/credentials/{credential_id}/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
        json=cred_update,
    )
    return response


def test_credential_update_status(api_client, api_keys, api_users, skills):
    """Test updating the status of a credential"""
    api_user1, api_user2 = api_users
    credential = {
        "holder": api_user1["id"],
        "skill": skills[api_user1["id"]][0]["id"],
        "issuer": api_user1["id"],
        "status": "Requested",
    }
    user_id = api_user1["id"]
    response = create_credential(api_client, api_keys, user_id, credential)
    assert response.status_code == 200
    cred_id = response.json["id"]

    # Modify status to Issued
    r_issued = update_credential_status(
        api_client, api_keys, api_user1["id"], cred_id, "Issued"
    )
    assert r_issued.status_code == 200
    assert r_issued.json["status"] in ["Issued", "Pending Issuance"]
    # Modify status to Revoked
    r_revoked = update_credential_status(
        api_client, api_keys, api_user1["id"], cred_id, "Revoked"
    )
    assert r_revoked.status_code == 200
    assert r_revoked.json["status"] in ["Revoked", "Pending Revocation"]


def test_credential_update_status_other(api_client, api_keys, api_users, skills):
    """Test updating the status of a credential"""
    api_user1, api_user2 = api_users
    credential = {
        "holder": api_user1["id"],
        "skill": skills[api_user1["id"]][0]["id"],
        "issuer": api_user2["id"],
        "status": "Requested",
    }
    user_id = api_user1["id"]
    response = create_credential(api_client, api_keys, user_id, credential)
    assert response.status_code == 200
    cred_id = response.json["id"]

    # Modify status to Issued
    # This should only be possible for user 2
    r_issued = update_credential_status(
        api_client, api_keys, api_user1["id"], cred_id, "Issued"
    )
    assert r_issued.status_code == 403


def test_credential_visible_for_holder(api_client, api_keys, api_users, skills):
    """Test that a credential made by user 1 about user 2 is visible to them"""
    api_user1, api_user2 = api_users
    credential = {
        "holder": api_user2["id"],
        "skill": skills[api_user1["id"]][0]["id"],
        "issuer": api_user1["id"],
        "status": "Issued",
    }
    user_id = api_user1["id"]
    response = create_credential(api_client, api_keys, user_id, credential)

    assert response.status_code == 200
    # Credential has been issued by user 1 to user 2
    # Check that user 2 can see it
    response2 = api_client.get(
        f"/api/v1/users/{api_user2['id']}/credentials/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
    )
    assert response2.status_code == 200
    assert "credentials" in response2.json.keys()
    assert response.json["id"] in [i["id"] for i in response2.json["credentials"]]


def test_credential_visible_for_request(api_client, api_keys, api_users, skills):
    """Test that a credential request is visible to the user being requested
    to issue the credential"""
    api_user1, api_user2 = api_users
    credential = {
        "holder": api_user1["id"],
        "skill": skills[api_user1["id"]][0]["id"],
        "issuer": api_user2["id"],
        "status": "Requested",
    }
    user_id = api_user1["id"]
    response = create_credential(api_client, api_keys, user_id, credential)
    assert response.status_code == 200
    # Credential has been requested by user 1 from user 2
    # Check that user 2 can see it
    response2 = api_client.get(
        f"/api/v1/users/{api_user2['id']}/credentials/",
        headers={"X-API-Key": api_keys.access, "X-Auth-Token": api_keys.secret},
    )
    assert response2.status_code == 200
    assert "credentials" in response2.json.keys()
    assert response.json["id"] in [i["id"] for i in response2.json["credentials"]]

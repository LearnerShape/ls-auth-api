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

from flask import current_app
import pdb
import random
import requests
import string
from urllib.parse import urljoin

from ls_auth_api import models
from ls_auth_api.models import db
from .word_list import word_list


def generate_passphrase(n=6, glue="-"):
    """Generate a passphrase

    This uses the EFF word list"""
    return glue.join(random.choices(word_list, k=n))


def _prepare_DID_creation(register_did=True):
    """Prepare the request for creating a new DID"""
    new_did = {"passphrase": generate_passphrase(), "register_did": register_did}
    return new_did


def create_DID(register_did=True):
    """Create a new DID"""
    new_did = _prepare_DID_creation(register_did=register_did)
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _create_DID_testing(new_did)
    return _create_DID_blockchain(new_did)


def _create_DID_testing(new_did):
    r = new_did.copy()
    r.update(
        {
            "mnemonic": [
                "midnight",
                "supreme",
                "hand",
                "pass",
                "kangaroo",
                "cage",
                "toddler",
                "beach",
                "liberty",
                "black",
                "large",
                "assist",
            ],
            "did_canonical": "did:prism:f78422a7c4d2f23016153e2e6262f3d093476b767c1b06f62f40c7623d3f5a2f",
            "did_long_form": "did:prism:f78422a7c4d2f23016153e2e6262f3d093476b767c1b06f62f40c7623d3f5a2f:Cr8BCrwBEjsKB21hc3RlcjAQAUouCglzZWNwMjU2azESIQMTAumLMPC9fU56QO6e4DTtbPwR1DHg9mCJrq_D4-IqBBI8Cghpc3N1aW5nMBACSi4KCXNlY3AyNTZrMRIhA4YfAbmK6VLiXh5VC3SERihfgh7DbcQryKyAMJlC3PaEEj8KC3Jldm9jYXRpb24wEAVKLgoJc2VjcDI1NmsxEiEDZWzXp2d-hQ9Vd_-tkvy7uQZAEFbi3fgvR66LvDK4GIM",
            "creation_operation_id": "ff7935a5274f639b6468670a1dc21d9150cbce6b624ca267351f154204b35282",
            "operation_hash": "0051feadbacd3f09194ea3a43fc5ebc11d23f71ddd47f713bbdd31faba18d12c",
        }
    )
    r["mnemonic"] = " ".join(r["mnemonic"])
    return r


def _create_DID_blockchain(new_did):
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "DID/"), json=new_did
    )
    assert r.status_code == 200
    result = r.json()
    result["mnemonic"] = " ".join(result["mnemonic"])
    return result


def check_DID_status(self, operation_id):
    """Check whether DID is registered on blockchain"""
    payload = {"creation_operation_id": operation_id}
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _check_DID_status_testing(operation_id)
    return _check_DID_status_blockchain(operation_id)


def _check_DID_status_testing(operation_id):
    payload = {"creation_operation_id": operation_id, "status": "CONFIRMED_AND_APPLIED"}
    return payload


def _check_DID_status_blockchain(operation_id):
    payload = {"creation_operation_id": operation_id}
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "DID_status/"),
        json=payload,
    )
    assert r.status_code == 200
    return r.json()


def _prepare_credential(credential):
    """Prepare the request for creating a new credential"""
    issuer_did = (
        models.DID.query.filter(models.DID.owner_id == credential.issuer_id)
        .filter(models.DID.primary == True)
        .all()
    )
    holder_did = (
        models.DID.query.filter(models.DID.owner_id == credential.holder_id)
        .filter(models.DID.primary == True)
        .all()
    )
    if len(issuer_did) != 1:
        abort(403)
    if len(holder_did) != 1:
        abort(403)
    issuer_did = issuer_did[0]
    holder_did = holder_did[0]
    skill = models.Skill.query.filter(models.Skill.id == credential.skill_id).first()
    return {
        "content": skill.skill_details,
        "holder_did": holder_did.DID,
        "issuer_mnemonic": issuer_did.mnemonic.split(" "),
        "issuer_passphrase": issuer_did.passphrase,
    }


def create_credential(credential):
    """Create a new credential"""
    new_credential = _prepare_credential(credential)
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _create_credential_testing(new_credential)
    return _create_credential_blockchain(new_credential)


def _create_credential_testing(new_credential):
    # TODO: Identify the key items to return when SDK is working
    r = new_credential.copy()
    r.update(
        {
            "creation_operation_id": "b284163a99905f8bb9c40bd56c7e0dd678b9689d88a1fdf5041001f5bd76b7be",
            "signed_credential_content": '{"id":"did:prism:0051feadbacd3f09194ea3a43fc5ebc11d23f71ddd47f713bbdd31faba18d12c","keyId":"issuing0","credentialSubject":{"name":"test","subject":"testing2","id":"did:prism:f78422a7c4d2f23016153e2e6262f3d093476b767c1b06f62f40c7623d3f5a2f"}}',
            "signed_credential_canonical": "eyJpZCI6ImRpZDpwcmlzbTowMDUxZmVhZGJhY2QzZjA5MTk0ZWEzYTQzZmM1ZWJjMTFkMjNmNzFkZGQ0N2Y3MTNiYmRkMzFmYWJhMThkMTJjIiwia2V5SWQiOiJpc3N1aW5nMCIsImNyZWRlbnRpYWxTdWJqZWN0Ijp7Im5hbWUiOiJ0ZXN0Iiwic3ViamVjdCI6InRlc3RpbmcyIiwiaWQiOiJkaWQ6cHJpc206Zjc4NDIyYTdjNGQyZjIzMDE2MTUzZTJlNjI2MmYzZDA5MzQ3NmI3NjdjMWIwNmY2MmY0MGM3NjIzZDNmNWEyZiJ9fQ.MEUCIFcWc6v1-2a_192lmdinURvm0IQ4ReA8Q5cZDI6gZS96AiEAwpbSkHun9Yh0PO7ZtUlhgjqR0GirmxwY4SJkROXwyYs",
            "signed_credential_proof": '{"hash":"22e7ca77fc1e526af82e9ee54ba97be5d19660718e168daccbf54f2f4ce26fda","index":0,"siblings":[]}',
        }
    )
    return r


def _create_credential_blockchain(new_credential):
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "credential/"),
        json=new_credential,
    )
    assert r.status_code == 200
    return r.json()


def check_credential_status(operation_id):
    """Check the status of a credential"""
    payload = {"creation_operation_id": operation_id}
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _check_DID_status_testing(operation_id)
    return _check_DID_status_blockchain(operation_id)


def _check_DID_status_testing(operation_id):
    payload = {"creation_operation_id": operation_id, "status": "CONFIRMED_AND_APPLIED"}
    return payload


def _check_DID_status_blockchain(operation_id):
    payload = {"creation_operation_id": operation_id}
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "credential_status/"),
        json=payload,
    )
    assert r.status_code == 200
    return r.json()

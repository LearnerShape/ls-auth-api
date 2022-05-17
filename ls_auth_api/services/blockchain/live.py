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
import requests
from urllib.parse import urljoin


def _create_DID_blockchain(new_did):
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "DID/"), json=new_did
    )
    assert r.status_code == 200
    result = r.json()
    result["mnemonic"] = " ".join(result["mnemonic"])
    return result


def _check_DID_status_blockchain(operation_id):
    payload = {"creation_operation_id": operation_id}
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "DID_status/"),
        json=payload,
    )
    assert r.status_code == 200
    return r.json()


def _create_credential_blockchain(new_credential):
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "credential/"),
        json=new_credential,
    )
    assert r.status_code == 200
    return r.json()


def _check_credential_status_blockchain(operation_id):
    payload = {"creation_operation_id": operation_id}
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "credential_status/"),
        json=payload,
    )
    assert r.status_code == 200
    return r.json()


def _verify_credential_blockchain(payload):
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "verify_credential/"),
        json=payload,
    )
    assert r.status_code == 200
    return r.json()


def _revoke_credential_blockchain(payload):
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "revoke_credential/"),
        json=payload,
    )
    assert r.status_code == 200
    return r.json()


def _check_credential_revocation_blockchain(operation_id):
    payload = {"revocation_operation_id": operation_id}
    r = requests.post(
        urljoin(
            current_app.config["BLOCKCHAIN_SERVICE_URI"],
            "credential_revocation_status/",
        ),
        json=payload,
    )
    assert r.status_code == 200
    return r.json()

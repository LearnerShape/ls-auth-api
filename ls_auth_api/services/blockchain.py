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
    f = lambda x: "".join(random.choices(string.digits + string.ascii_lowercase, k=x))
    r.update(
        {
            "seed": f(100),
            "did_canonical": "did:prism:" + f(62),
            "creation_operation_id": random.randint(0, 1e8),
            "hash": f(50),
        }
    )
    r.update({"did_long_form": r["did_canonical"] + ":" + f(86)})
    return r


def _create_DID_blockchain(new_did):
    r = requests.post(
        urljoin(current_app.config["BLOCKCHAIN_SERVICE_URI"], "DID"), json=new_did
    )
    assert r.status_code == 200
    return r.json


def check_DID_status(self, operation_id):
    """Check whether DID is registered on blockchain"""
    pass


def create_credential(self):
    """Create a new credential"""
    pass


def check_credential_status(self):
    """Check the status of a credential"""
    pass

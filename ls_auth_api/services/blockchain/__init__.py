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

from ls_auth_api import models
from ls_auth_api.models import db
from .word_list import word_list
from .testing import (
    _create_DID_testing,
    _check_DID_status_testing,
    _create_credential_testing,
    _check_credential_status_testing,
    _verify_credential_testing,
    _revoke_credential_testing,
    _check_credential_revocation_testing,
)

from .live import (
    _create_DID_blockchain,
    _check_DID_status_blockchain,
    _create_credential_blockchain,
    _check_credential_status_blockchain,
    _verify_credential_blockchain,
    _revoke_credential_blockchain,
    _check_credential_revocation_blockchain,
)


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


def check_DID_status(self, operation_id):
    """Check whether DID is registered on blockchain"""
    payload = {"creation_operation_id": operation_id}
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _check_DID_status_testing(operation_id)
    return _check_DID_status_blockchain(operation_id)


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


def check_credential_status(operation_id):
    """Check the status of a credential"""
    payload = {"creation_operation_id": operation_id}
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _check_credential_status_testing(operation_id)
    return _check_credential_status_blockchain(operation_id)


def _prepare_verify_credential(credential):
    """Prepare the request to verify a credential"""
    payload = {
        "signed_credential": credential.signed_credential_canonical,
        "signed_credential_proof": credential.signed_credential_proof,
    }
    return payload


def verify_credential(credential):
    """Verify current status of a credential"""
    payload = _prepare_verify_credential(credential)
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _verify_credential_testing(operation_id)
    return _verify_credential_blockchain(operation_id)


def _prepare_credential_revocation(credential):
    """Prepare the request to revoke a credential"""
    issuer_did = (
        models.DID.query.filter(models.DID.owner_id == credential.issuer_id)
        .filter(models.DID.primary == True)
        .all()
    )
    if len(issuer_did) != 1:
        abort(403)
    issuer_did = issuer_did[0]
    payload = {
        "issuer_mnemonic": issuer_did.mnemonic,
        "issuer_passphrase": issuer_did.passphrase,
        "operation_hash": credential.creation_operation_hash,
        "batch_id": credential.batch_id,
        "signed_credential_hash": credential.signed_credential_hash,
    }
    return payload


def revoke_credential(credential):
    """Revoke a credential"""
    payload = _prepare_credential_revocation(credential)
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _revoke_credential_testing(operation_id)
    return _revoke_credential_blockchain(operation_id)


def check_credential_revocation(operation_id):
    """Check status of credential revocation request"""
    payload = {"creation_operation_id": operation_id}
    if not current_app.config["INTERACT_WITH_BLOCKCHAIN"]:
        return _check_credential_revocation_testing(operation_id)
    return _check_credential_revocation_blockchain(operation_id)

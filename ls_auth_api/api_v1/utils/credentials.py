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
from celery import shared_task
from datetime import datetime
from flask import abort

from ls_auth_api import models
from ls_auth_api.models import db
from ls_auth_api.services import blockchain


def format_credential(credential):
    """Format a credential record to the schema"""
    return {
        i: credential.__getattribute__(j)
        for i, j in [
            ["id", "id"],
            ["skill", "skill_id"],
            ["issuer", "issuer_id"],
            ["status", "status"],
            ["holder", "holder_id"],
            ["creation_date", "creation_date"],
            ["submission_date", "submission_date"],
            ["submission_transaction_id", "submission_transaction_id"],
            ["revocation_date", "revocation_date"],
            ["revocation_transaction_id", "revocation_transaction_id"],
            ["last_check_date", "last_check_date"],
        ]
    }


def get_details(user_uuid, credential_id=None):
    """Get schema-formatted details on credentials"""
    credentials = models.Credential.query.filter(
        (models.Credential.holder_id == user_uuid)
        | (models.Credential.issuer_id == user_uuid)
    )
    if credential_id:
        credentials = credentials.filter(models.Credential.id.in_(credential_id))
    credentials = credentials.all()
    output = []
    for cred in credentials:
        output.append(format_credential(cred))
    return output


def _update_db_from_blockchain(credential, blockchain):
    credential.signed_credential_content = blockchain["signed_credential_content"]
    credential.signed_credential_canonical = blockchain["signed_credential_canonical"]
    credential.signed_credential_proof = blockchain["signed_credential_proof"]
    credential.creation_operation_id = blockchain["creation_operation_id"]
    credential.signed_credential_hash = blockchain["signed_credential_hash"]
    credential.creation_operation_hash = blockchain["operation_hash"]
    credential.batch_id = blockchain["batch_id"]
    return credential


def _update_db_from_blockchain_revoke(credential, blockchain):
    credential.revocation_operation_id = blockchain["revocation_operation_id"]
    return credential


def create(user_uuid, credential_data):
    """Create a new credential"""
    if user_uuid not in [credential_data["issuer"], credential_data["holder"]]:
        abort(403)
    if credential_data["status"] not in ["Requested", "Issued"]:
        abort(403)
    if (credential_data["status"] == "Issued") and (
        credential_data["issuer"] != user_uuid
    ):
        abort(403)
    new_credential = models.Credential(
        skill_id=credential_data["skill"],
        issuer_id=credential_data["issuer"],
        holder_id=credential_data["holder"],
        status=credential_data["status"],
        creation_date=datetime.now(),
    )
    if credential_data["status"] == "Issued":
        blockchain_credential = blockchain.create_credential(new_credential)
        new_credential = _update_db_from_blockchain(
            new_credential, blockchain_credential
        )
        new_credential.status = "Pending Issuance"
        new_credential.submission_date = datetime.now()
    db.session.add(new_credential)
    db.session.commit()
    if new_credential.status == "Pending Issuance":
        check_issuance_status.apply_async((new_credential.id,), countdown=2 * 60)
    return format_credential(new_credential)


def update(user_uuid, credential_uuid, credential_data):
    """Update the status of a credential"""
    current_credential = models.Credential.query.filter(
        models.Credential.id == credential_uuid
    ).first()
    current_status = current_credential.status
    new_status = credential_data["status"]
    if current_credential.issuer_id != user_uuid:
        abort(403)
    if (current_status == "Requested") and (new_status == "Issued"):
        # Issue credential
        blockchain_credential = blockchain.create_credential(current_credential)
        current_credential = _update_db_from_blockchain(
            current_credential, blockchain_credential
        )
        current_credential.status = "Pending Issuance"
        current_credential.submission_date = datetime.now()
        check_issuance_status.apply_async((current_credential.id,), countdown=2 * 60)
    elif (current_status == "Issued") and (new_status == "Revoked"):
        # Revoke credential
        blockchain_revoke = blockchain.revoke_credential
        current_credential = _update_db_from_blockchain_revoke(
            current_credential, blockchain_revoke
        )
        current_credential.status = "Pending Revocation"
        current_credential.revocation_date = datetime.now()
        check_revocation_status.apply_async((current_credential.id,), countdown=2 * 60)
    else:
        # Requested transition is not available
        abort(409)
    db.session.add(current_credential)
    db.session.commit()
    return current_credential


@shared_task
def check_issuance_status(credential_uuid):
    cred = models.Credential.query.filter(
        models.Credential.id == credential_uuid
    ).first()
    try:
        results = blockchain.check_credential_status(cred.creation_operation_id)
    except:
        check_issuance_status.apply_async((credential_uuid,), countdown=2 * 60)
        return
    if results["status"] != "CONFIRMED_AND_APPLIED":
        # Check later
        check_issuance_status.apply_async((credential_uuid,), countdown=2 * 60)
        return
    cred.status = "Issued"
    cred.submission_transaction_id = results["transaction_id"]
    db.session.add(cred)
    db.session.commit()


@shared_task
def verify_status(credential_uuid):
    cred = models.Credential.query.filter(
        models.Credential.id == credential_uuid
    ).first()
    try:
        results = blockchain.verify_credential(cred)
    except:
        verify_status.apply_async((credential_uuid,), countdown=2 * 60)
        return
    if len(results["errors"]) > 0:
        cred.status = "Revoked"
    cred.last_check_date = datetime.now()
    db.session.add(cred)
    db.session.commit()


@shared_task
def check_revocation_status(credential_uuid):
    cred = models.Credential.query.filter(
        models.Credential.id == credential_uuid
    ).first()
    try:
        results = blockchain.check_credential_revocation(cred.revocation_operation_id)
    except:
        check_revocation_status.apply_async((credential_uuid,), countdown=2 * 60)
        return
    if results["status"] != "CONFIRMED_AND_APPLIED":
        # Check later
        check_revocation_status.apply_async((credential_uuid,), countdown=2 * 60)
        return
    cred.status = "Revoked"
    cred.revocation_transaction_id = results["transaction_id"]
    db.session.add(cred)
    db.session.commit()

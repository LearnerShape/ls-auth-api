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
from celery import shared_task
from datetime import datetime
from flask import abort
import pdb

from ls_auth_api import models
from ls_auth_api.models import db
from ls_auth_api.services import blockchain


def format_DID(DID):
    """Format a DID record to the schema"""
    return {
        i: DID.__getattribute__(j)
        for i, j in [
            ["id", "id"],
            ["DID", "DID"],
            ["owner", "owner_id"],
            ["primary", "primary"],
            ["status", "status"],
            ["creation_date", "creation_date"],
            ["submission_date", "submission_date"],
            ["submission_transaction_id", "submission_transaction_id"],
            ["last_check_date", "last_check_date"],
        ]
    }


def get_details(user_uuid, DID_id=None):
    """Get schema-formatted details on DIDs"""
    DIDs = models.DID.query.filter(models.DID.owner_id == user_uuid)
    if DID_id:
        DIDs = DIDs.filter(models.DID.id.in_(DID_id))
    DIDs = DIDs.all()
    output = []
    for DID in DIDs:
        output.append(format_DID(DID))
    return output


def create(user_uuid, DID_data):
    """Create a new DID"""
    if user_uuid != DID_data["owner"]:
        abort(403)
    if DID_data["status"] not in ["Published", "Unpublished"]:
        abort(403)
    if DID_data["primary"] == True:
        existing_DIDs = models.DID.query.filter(models.DID.owner_id == user_uuid).all()
        for i in existing_DIDs:
            if i.primary == True:
                i.primary = False
                db.session.add(i)
    new_DID = models.DID(
        owner_id=user_uuid,
        primary=DID_data["primary"],
        status="Unpublished",
        creation_date=datetime.now(),
    )
    register_did = True if (DID_data["status"] == "Published") else False
    if register_did:
        new_DID.status = "Pending publication"
    db.session.add(new_DID)
    db.session.commit()
    register_DID.apply_async(
        (new_DID.id,),
    )
    return format_DID(new_DID)


@shared_task
def register_DID(DID_id):
    """Create/register a DID"""
    new_DID = models.DID.query.filter(models.DID.id == DID_id).first()
    register_did = True if (new_DID.status == "Pending publication") else False
    try:
        blockchain_did = blockchain.create_DID(register_did=register_did)
    except:
        register_DID.apply_async((DID_id,), countdown=2 * 60)
        return
    new_DID.DID = blockchain_did["did_canonical"]
    new_DID.did_long_form = blockchain_did["did_long_form"]
    new_DID.mnemonic = blockchain_did["mnemonic"]
    new_DID.passphrase = blockchain_did["passphrase"]
    if register_did:
        new_DID.creation_operation_id = blockchain_did["creation_operation_id"]
        new_DID.state_hash = blockchain_did["operation_hash"]
        # new_DID.status = "Pending publication"
        new_DID.submission_date = datetime.now()
    db.session.add(new_DID)
    db.session.commit()
    check_DID_status.apply_async((new_DID.id,), countdown=2 * 60)


@shared_task
def check_DID_status(DID_id):
    DID = models.DID.query.filter(models.DID.id == DID_id).first()
    try:
        results = blockchain.check_DID_status(DID.creation_operation_id)
    except:
        check_DID_status.apply_async((DID.id,), countdown=2 * 60)
        return
    if results["status"] != "CONFIRMED_AND_APPLIED":
        check_DID_status.apply_async((DID.id,), countdown=2 * 60)
        return
    DID.status = "Published"
    DID.submission_transaction_id = results["transaction_id"]
    DID.last_check_date = datetime.now()
    db.session.add(DID)
    db.session.commit()

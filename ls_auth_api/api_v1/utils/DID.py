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

from flask import abort
import pdb

from ls_auth_api import models
from ls_auth_api.models import db
from ls_auth_api.services import create_DID


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
        owner_id=user_uuid, primary=DID_data["primary"], status="Unpublished"
    )
    register_did = True if (DID_data["status"] == "Published") else False
    blockchain_did = create_DID(register_did=register_did)
    new_DID.DID = blockchain_did["did_canonical"]
    new_DID.did_long_form = blockchain_did["did_long_form"]
    new_DID.seed = blockchain_did["seed"]
    new_DID.passphrase = blockchain_did["passphrase"]
    if register_did:
        new_DID.creation_operation_id = blockchain_did["creation_operation_id"]
        new_DID.state_hash = blockchain_did["hash"]
        new_DID.status = "Pending publication"
    db.session.add(new_DID)
    db.session.commit()
    return format_DID(new_DID)

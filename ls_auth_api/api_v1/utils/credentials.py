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
from flask import abort

from ls_auth_api import models
from ls_auth_api.models import db


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
    )
    db.session.add(new_credential)
    db.session.commit()
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
        current_credential.status = new_status
        db.session.add(current_credential)
        db.session.commit()
        # TODO: blockchain integration
    elif (current_status == "Issued") and (new_status == "Revoked"):
        # Revoke credential
        current_credential.status = new_status
        db.session.add(current_credential)
        db.session.commit()
        # TODO blockchain integration
    else:
        # Requested transition is not available
        abort(409)
    return current_credential

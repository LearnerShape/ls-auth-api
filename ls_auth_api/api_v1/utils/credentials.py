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

from ls_auth_api import models
from ls_auth_api.models import db


def format_credential(credential):
    """Format a credential record to the schema"""
    return {
        i: credential.__getattribute__(i)
        for i in ["id", "skill", "issuer", "status", "holder"]
    }


def get_details(user_uuid, credential_id=None):
    """Get schema-formatted details on credentials"""
    credentials = models.Credential.query.filter(models.Credential.holder == user_uuid)
    if credential_id:
        credentials = credentials.filter(models.Credential.id.in_(credential_id))
    credentials = credentials.all()
    output = []
    for cred in credentials:
        output.append(format_credential(cred))
    return output


def create(user_uuid, credential_data):
    """Create a new credential"""
    new_credential = models.Credential(
        skill=credential_data["skill"],
        issuer=credential_data["issuer"],
        status=credential_data["status"],
        holder=credential_data["holder"],
    )
    db.session.add(new_credential)
    db.session.commit()
    return format_credential(new_credential)

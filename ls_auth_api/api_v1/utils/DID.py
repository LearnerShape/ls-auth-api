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
    new_DID = models.DID(
        owner_id=user_uuid,
        primary=DID_data["primary"],
        status=DID_data["status"],
    )
    db.session.add(new_DID)
    db.session.commit()
    return format_DID(new_DID)

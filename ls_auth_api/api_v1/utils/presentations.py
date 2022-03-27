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


def format_presentation(presentation):
    """Format a presentation record to the schema"""
    return {
        i: presentation.__getattribute__(j)
        for i, j in [
            ["id", "id"],
            ["owner", "owner_id"],
        ]
    }


def get_details(user_uuid, presentation_id=None):
    """Get schema-formatted details on presentationss"""
    presentations = models.Presentation.query.filter(
        models.Presentation.owner_id == user_uuid
    )
    if presentation_id:
        presentations = presentations.filter(
            models.Presentation.id.in_(presentation_id)
        )
    presentations = presentations.all()
    output = []
    for presentation in presentations:
        output.append(format_presentation(presentation))
    return output


def create(user_uuid, presentation_data):
    """Create a new presentation"""
    new_presentation = models.Presentation(
        owner_id=user_uuid,
    )
    db.session.add(new_presentation)
    db.session.commit()
    return format_presentation(new_presentation)

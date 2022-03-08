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


def format_skill(skill):
    """Format a skill record to the schema"""
    return {
        i: skill.__getattribute__(i)
        for i in ["id", "author_id", "skill_type", "skill_details"]
    }


def get_details(user_uuid, skill_id=None):
    """Get schema-formatted details on skills"""
    skills = models.Skill.query.filter(models.Skill.author_id == user_uuid)
    if skill_id:
        skills = skills.filter(models.Skill.id.in_(skill_id))
    skills = skills.all()
    output = []
    for skill in skills:
        output.append(format_skill(skill))
    return output


def create(user_uuid, skill_data):
    """Create a new skill"""
    new_skill = models.Skill(
        author_id=user_uuid,
        skill_type=skill_data["skill_type"],
        skill_details=skill_data["skill_details"],
    )
    db.session.add(new_skill)
    db.session.commit()
    return format_skill(new_skill)

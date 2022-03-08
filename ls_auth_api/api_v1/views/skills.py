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

from flask.views import MethodView
from flask import g
from flask_smorest import abort
from marshmallow import ValidationError

import pdb

from ls_auth_api.api_v1 import api
from ls_auth_api.api_v1.schemas import SkillSchema, SkillManySchema
from ls_auth_api.api_v1.utils import skills as skill_utils


@api.route("users/<user_uuid>/skills/")
class SkillsAPI(MethodView):
    @api.response(200, SkillManySchema)
    def get(self, user_uuid):
        """Get Skills

        Get a list of skills for a user"""
        skills = skill_utils.get_details(user_uuid)
        return {"skills": skills}

    @api.arguments(SkillSchema, location="json")
    @api.response(200, SkillSchema)
    def post(self, skill_data, user_uuid):
        """Create skill

        Create a new skill"""
        new_skill = skill_utils.create(user_uuid, skill_data)
        return new_skill


@api.route("users/<user_uuid>/skills/<skill_uuid>/")
class SkillDetailAPI(MethodView):
    @api.response(200, SkillSchema)
    def get(self, user_uuid, skill_uuid):
        """Get skill detail

        Get detailed information on a skill"""
        skill = skill_utils.get_details(
            user_uuid,
            [
                skill_uuid,
            ],
        )
        return skill[0]

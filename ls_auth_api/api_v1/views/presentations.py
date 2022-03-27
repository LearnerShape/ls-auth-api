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
from ls_auth_api.api_v1.schemas import PresentationSchema, PresentationManySchema
from ls_auth_api.api_v1.utils import presentations as presentation_utils


@api.route("users/<user_uuid>/presentations/")
class PresentationsAPI(MethodView):
    @api.response(200, PresentationManySchema)
    def get(self, user_uuid):
        """Get Presentationss

        Get a list of verifiable presentations for a user"""
        presentations = presentation_utils.get_details(user_uuid)
        return {"presentations": presentations}

    @api.arguments(PresentationSchema, location="json")
    @api.response(200, PresentationSchema)
    def post(self, presentation_data, user_uuid):
        """Create a new presentation"""
        new_presentation = presentation_utils.create(user_uuid, presentation_data)
        return new_presentation


@api.route("users/<user_uuid>/presentations/<presentation_uuid>/")
class PresentationDetailAPI(MethodView):
    @api.response(200, PresentationSchema)
    def get(self, user_uuid, presentation_uuid):
        """Get presentation detail

        Get detailed information on a verifiable presentation"""
        presentation = presentation_utils.get_details(
            user_uuid,
            [
                presentation_uuid,
            ],
        )
        return presentation[0]

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
import uuid
import pdb

from ls_auth_api.api_v1 import api
from ls_auth_api.api_v1.schemas import DIDSchema, DIDManySchema
from ls_auth_api.api_v1.utils import DID as DID_utils


@api.route("users/<user_uuid>/DIDs/")
class DIDsAPI(MethodView):
    @api.response(200, DIDManySchema)
    def get(self, user_uuid):
        """Get DIDs

        Get a list of DIDs for a user"""
        user_uuid = uuid.UUID(user_uuid)
        DIDs = DID_utils.get_details(user_uuid)
        return {"DIDs": DIDs}

    @api.arguments(DIDSchema, location="json")
    @api.response(200, DIDSchema)
    def post(self, DID_data, user_uuid):
        """Create a DID

        Create a new DID"""
        user_uuid = uuid.UUID(user_uuid)
        new_DID = DID_utils.create(user_uuid, DID_data)
        return new_DID


@api.route("users/<user_uuid>/DIDs/<DID_uuid>/")
class DIDDetailAPI(MethodView):
    @api.response(200, DIDSchema)
    def get(self, user_uuid, DID_uuid):
        """Get DID detail

        Get detailed information on a DID"""
        user_uuid = uuid.UUID(user_uuid)
        DID = DID_utils.get_details(
            user_uuid,
            [
                DID_uuid,
            ],
        )
        return DID[0]

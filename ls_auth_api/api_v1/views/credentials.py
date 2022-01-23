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
from ls_auth_api.api_v1.schemas import CredentialSchema, CredentialManySchema
from ls_auth_api.api_v1.utils import credentials as credential_utils


@api.route("users/<user_uuid>/credentials/")
class CredentialsAPI(MethodView):
    @api.response(200, CredentialManySchema)
    def get(self, user_uuid):
        """Get Credentials

        Get a list of credentails for a user"""
        credentials = credential_utils.get_details(user_uuid)
        return {"credentials": credentials}

    @api.arguments(CredentialSchema, location="json")
    @api.response(200, CredentialSchema)
    def post(self, credential_data, user_uuid):
        """Create credential

        Create a new credential"""
        new_credential = credential_utils.create(user_uuid, credential_data)
        return new_credential

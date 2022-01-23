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

from ls_auth_api.api_v1 import api
from ls_auth_api.api_v1.schemas import CredentialSchema, CredentialManySchema


@api.route("users/<user_uuid>/credentials/")
class CredentialsAPI(MethodView):
    @api.response(200, CredentialManySchema)
    def get(self):
        """Get Credentials

        Get a list of credentails for a user"""
        pass

    @api.arguments(CredentialSchema, location="json")
    @api.response(200, CredentialSchema)
    def post(self, credential_data):
        """Create credential

        Create a new credential"""
        pass

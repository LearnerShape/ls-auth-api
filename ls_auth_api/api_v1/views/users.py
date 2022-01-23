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

from ls_auth_api import models
from ls_auth_api.models import db
from ls_auth_api.api_v1 import api
from ls_auth_api.api_v1.schemas import UserSchema, UserManySchema
from ls_auth_api.api_v1.utils import users as user_utils


@api.route("users/")
class UsersAPI(MethodView):
    @api.response(200, UserManySchema)
    def get(self):
        """Get Users

        Get a list of all users"""
        users = user_utils.get_details()
        return {"users": users}

    @api.arguments(UserSchema, location="json")
    @api.response(200, UserSchema)
    def post(self, user_data):
        """Create user

        Create a new user"""
        new_user = user_utils.create(user_data)
        return new_user

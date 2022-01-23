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


def format_user(u):
    return {i: u.__getattribute__(i) for i in ["id", "name", "email"]}


def get_details(user_id=None):
    """Get schema-formatted details on users"""
    users = models.User.query
    if user_id:
        users = users.filter(models.User.id.in_(user_id))
    users = users.all()
    for u in users:
        yield format_user(u)


def create(data):
    """Create a new user"""
    new_user = models.User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return format_user(new_user)

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


from flask import current_app, g, request
from flask_smorest import abort, Blueprint
from werkzeug.exceptions import default_exceptions


api = Blueprint("api_v1", __name__, url_prefix="/api/v1", description="API version 1")


@api.before_request
def require_access_headers():
    """Require that appropriate headers are set"""
    if request.path in []:
        # List of paths that do not require access headers
        return
    access_id = request.headers.get("X-API-Key")
    access_secret = request.headers.get("X-Auth-Token")
    if not access_id or not access_secret:
        abort(403)
    auth_access, auth_secret = (
        current_app.config["API_ACCESS_ID"],
        current_app.config["API_SECRET_KEY"],
    )
    if (access_id != auth_access) or (access_secret != auth_secret):
        abort(403)


from .views import *

for ex in default_exceptions:
    api.register_error_handler(ex, handle_error)

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

from collections import namedtuple
import pdb
import pytest


from ls_auth_api import create_app

access_id, secret_key = "a", "b"


@pytest.fixture(scope="module")
def api_client():
    app = create_app()
    app.config["API_ACCESS_ID"], app.config["API_SECRET_KEY"] = access_id, secret_key
    with app.test_client() as client:
        yield client


@pytest.fixture()
def api_keys():
    auth = namedtuple("auth", ["access", "secret"])
    yield auth(access_id, secret_key)

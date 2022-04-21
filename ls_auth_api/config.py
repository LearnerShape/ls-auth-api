# Copyright (C) 2021  Learnershape and contributors

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

import os

# Environment config
ENV = "development"
SECRET_KEY = "DEVELOPMENT"

# Database config
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", "postgresql://postgres@localhost:5432/postgres"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Blockchain config
BLOCKCHAIN_SERVICE_URI = os.environ.get("BLOCKCHAIN_SERVICE_URI", "http://blockchain/")
INTERACT_WITH_BLOCKCHAIN = (
    True
    if (
        os.environ.get(
            "INTERACT_WITH_BLOCKCHAIN",
        )
        in ["True", "true"]
    )
    else False
)

# API config
API_ACCESS_ID = os.environ.get(
    "API_ACCESS_ID",
)
API_SECRET_KEY = os.environ.get("API_SECRET_KEY")
if ENV != "development":
    assert API_ACCESS_ID, "API Access ID must be configured"
    assert API_SECRET_KEY, "API Secret key must be configured"

# Documentation config
API_TITLE = "Learnershape Skills Authentication API"
API_VERSION = "1"
OPENAPI_VERSION = "3.0.2"
OPENAPI_JSON_PATH = "api-spec.json"
OPENAPI_URL_PREFIX = "/"
OPENAPI_REDOC_PATH = "/redoc"
OPENAPI_REDOC_URL = (
    "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
)
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
OPENAPI_RAPIDOC_PATH = "/rapidoc"
OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

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

from marshmallow import fields

from .shared import OrderedBaseSchema


class CredentialSchema(OrderedBaseSchema):
    id = fields.UUID(dump_only=True)
    holder = fields.UUID()
    skill = fields.UUID()
    issuer = fields.UUID()
    status = fields.String()
    creation_date = fields.DateTime()
    submission_date = fields.DateTime()
    submission_transaction_id = fields.String()
    revocation_date = fields.DateTime()
    revocation_transaction_id = fields.String()
    last_check_date = fields.DateTime()


class CredentialManySchema(OrderedBaseSchema):
    credentials = fields.List(fields.Nested(lambda: CredentialSchema))


class CredentialUpdateSchema(OrderedBaseSchema):
    status = fields.String()

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


from sqlalchemy.dialects.postgresql import UUID
import uuid

from . import db


class DID(db.Model):
    """A DID record

    A distributed ID for use in credential creation"""

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    DID = db.Column(db.Text)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    primary = db.Column(db.Boolean)
    status = db.Column(db.Text)
    mnemonic = db.Column(db.Text)
    passphrase = db.Column(db.Text)
    did_long_form = db.Column(db.Text)
    creation_operation_id = db.Column(db.Text)
    state_hash = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    submission_date = db.Column(db.DateTime)
    submission_transaction_id = db.Column(db.Text)
    last_check_date = db.Column(db.DateTime)

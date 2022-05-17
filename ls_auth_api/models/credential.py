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


class Credential(db.Model):
    """A credential record"""

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    skill_id = db.Column(UUID(as_uuid=True), db.ForeignKey("skill.id"))
    issuer_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    status = db.Column(db.Text)
    holder_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    signed_credential_content = db.Column(db.Text)
    signed_credential_canonical = db.Column(db.Text)
    signed_credential_proof = db.Column(db.Text)
    signed_credential_hash = db.Column(db.Text)
    batch_id = db.Column(db.Text)
    creation_operation_id = db.Column(db.Text)
    creation_operation_hash = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    submission_date = db.Column(db.DateTime)
    submission_transaction_id = db.Column(db.Text)
    revocation_operation_id = db.Column(db.Text)
    revocation_date = db.Column(db.DateTime)
    revocation_transaction_id = db.Column(db.Text)
    last_check_date = db.Column(db.DateTime)

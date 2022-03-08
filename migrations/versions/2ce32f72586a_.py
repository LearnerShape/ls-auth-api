"""Create skill

Revision ID: 2ce32f72586a
Revises: 4a0e2c16ba08
Create Date: 2022-03-01 20:45:43.935790

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2ce32f72586a"
down_revision = "4a0e2c16ba08"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "skill",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("skill_type", sa.Text(), nullable=True),
        sa.Column("skill_details", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.add_column(
        "credential",
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "credential",
        sa.Column("issuer_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "credential",
        sa.Column("holder_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.drop_constraint("credential_holder_fkey", "credential", type_="foreignkey")
    op.drop_constraint("credential_issuer_fkey", "credential", type_="foreignkey")
    op.create_foreign_key(None, "credential", "user", ["holder_id"], ["id"])
    op.create_foreign_key(None, "credential", "user", ["issuer_id"], ["id"])
    op.create_foreign_key(None, "credential", "skill", ["skill_id"], ["id"])
    op.drop_column("credential", "holder")
    op.drop_column("credential", "issuer")
    op.drop_column("credential", "skill")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "credential", sa.Column("skill", sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "credential",
        sa.Column("issuer", postgresql.UUID(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "credential",
        sa.Column("holder", postgresql.UUID(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "credential", type_="foreignkey")
    op.drop_constraint(None, "credential", type_="foreignkey")
    op.drop_constraint(None, "credential", type_="foreignkey")
    op.create_foreign_key(
        "credential_issuer_fkey", "credential", "user", ["issuer"], ["id"]
    )
    op.create_foreign_key(
        "credential_holder_fkey", "credential", "user", ["holder"], ["id"]
    )
    op.drop_column("credential", "holder_id")
    op.drop_column("credential", "issuer_id")
    op.drop_column("credential", "skill_id")
    op.drop_table("skill")
    # ### end Alembic commands ###

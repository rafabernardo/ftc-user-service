"""Create users table

Revision ID: 9ab391020287
Revises: 9dc82bc010d1
Create Date: 2025-02-06 20:46:37.990238

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ab391020287"
down_revision: Union[str, None] = "9dc82bc010d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column(
            "is_admin", sa.Boolean(), server_default="false", nullable=False
        ),
        sa.Column(
            "is_reader", sa.Boolean(), server_default="true", nullable=False
        ),
        sa.Column(
            "is_editor", sa.Boolean(), server_default="false", nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("ix_users_email", "email", unique=True),
    )


def downgrade() -> None:
    op.drop_table("users")

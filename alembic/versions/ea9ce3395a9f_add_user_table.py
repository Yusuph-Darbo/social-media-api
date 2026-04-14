"""add user table

Revision ID: ea9ce3395a9f
Revises: b5381e301d58
Create Date: 2026-04-14 11:50:53.117422

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ea9ce3395a9f"
down_revision: Union[str, Sequence[str], None] = "b5381e301d58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        schema="social_media_api",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

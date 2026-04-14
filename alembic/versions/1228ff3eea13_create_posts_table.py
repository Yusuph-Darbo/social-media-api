"""create posts table

Revision ID: 1228ff3eea13
Revises:
Create Date: 2026-04-12 19:24:09.452167

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1228ff3eea13"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS social_media_api")
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "published", sa.Boolean(), server_default=sa.text("TRUE"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        schema="social_media_api",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts", schema="social_media_api")
    op.execute("DROP SCHEMA IF EXISTS social_media_api")

"""modify posts table

Revision ID: b5381e301d58
Revises: 1228ff3eea13
Create Date: 2026-04-14 10:55:06.846752

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b5381e301d58"
down_revision: Union[str, Sequence[str], None] = "1228ff3eea13"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "tag",
            sa.String(),
        ),
        schema="social_media_api",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "tag", schema="social_media_api")

"""add foreign key to posts

Revision ID: 5a1a991fa188
Revises: ea9ce3395a9f
Create Date: 2026-04-14 14:12:39.140390

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5a1a991fa188"
down_revision: Union[str, Sequence[str], None] = "ea9ce3395a9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False),
        schema="social_media_api",
    )
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        source_schema="social_media_api",
        referent_schema="social_media_api",
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")

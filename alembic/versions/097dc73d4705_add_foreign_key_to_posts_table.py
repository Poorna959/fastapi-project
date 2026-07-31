"""add foreign-key to posts table

Revision ID: 097dc73d4705
Revises: 5b930d25b8ec
Create Date: 2026-08-01 00:38:08.632535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '097dc73d4705'
down_revision: Union[str, Sequence[str], None] = '5b930d25b8ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("user_id", sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],      # <-- Fix here
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "posts_users_fk",
        "posts",
        type_="foreignkey"
    )

    op.drop_column("posts", "user_id") 

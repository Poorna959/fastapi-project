"""add content column to posts table

Revision ID: 7410c504be21
Revises: 8b649f54b9ce
Create Date: 2026-08-01 00:18:01.817544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7410c504be21'
down_revision: Union[str, Sequence[str], None] = '8b649f54b9ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass

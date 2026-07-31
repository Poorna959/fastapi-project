"""create posts table

Revision ID: 8b649f54b9ce
Revises: 
Create Date: 2026-08-01 00:07:36.895009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b649f54b9ce'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False)) 


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    

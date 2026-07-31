"""add users table

Revision ID: 5b930d25b8ec
Revises: 7410c504be21
Create Date: 2026-08-01 00:23:55.596036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b930d25b8ec'
down_revision: Union[str, Sequence[str], None] = '7410c504be21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
    'users',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False
    ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass

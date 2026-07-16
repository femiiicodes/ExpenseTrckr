"""add role to user schema

Revision ID: 31182bf2bea1
Revises: 7c469fe48e65
Create Date: 2026-05-25 13:23:25.557358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31182bf2bea1'
down_revision: Union[str, Sequence[str], None] = '7c469fe48e65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('role',sa.String))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','role')

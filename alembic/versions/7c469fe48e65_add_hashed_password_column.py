"""add hashed password column

Revision ID: 7c469fe48e65
Revises: 
Create Date: 2026-05-20 14:51:36.035283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c469fe48e65'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('hashed_password',sa.String))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','hashed_password')

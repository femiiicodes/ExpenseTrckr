"""edit time column

Revision ID: 8537684866f7
Revises: 31182bf2bea1
Create Date: 2026-05-26 12:01:17.480258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8537684866f7'
down_revision: Union[str, Sequence[str], None] = '31182bf2bea1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('expenses',schema=None) as batch_op:
        batch_op.alter_column('time',type_=sa.DateTime)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('expenses',schema=None) as batch_op:
        batch_op.alter_column('time',type_=sa.String)
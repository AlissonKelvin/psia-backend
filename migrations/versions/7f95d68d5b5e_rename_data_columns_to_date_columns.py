"""rename data columns to date columns

Revision ID: 7f95d68d5b5e
Revises: 3d42525000f1
Create Date: 2026-05-12 15:41:07.880185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7f95d68d5b5e'
down_revision: Union[str, Sequence[str], None] = '3d42525000f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'data_created', new_column_name='date_created')
    op.alter_column('users', 'data_updated', new_column_name='date_updated')

    op.alter_column('patients', 'data_created', new_column_name='date_created')
    op.alter_column('patients', 'data_updated', new_column_name='date_updated')

    op.alter_column(
        'journal_entries',
        'data_created',
        new_column_name='date_created',
    )
    op.alter_column(
        'journal_entries',
        'data_updated',
        new_column_name='date_updated',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'date_created', new_column_name='data_created')
    op.alter_column('users', 'date_updated', new_column_name='data_updated')

    op.alter_column('patients', 'date_created', new_column_name='data_created')
    op.alter_column('patients', 'date_updated', new_column_name='data_updated')

    op.alter_column(
        'journal_entries',
        'date_created',
        new_column_name='data_created',
    )
    op.alter_column(
        'journal_entries',
        'date_updated',
        new_column_name='data_updated',
    )
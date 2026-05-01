"""add_category_to_notes

Revision ID: fcc81d767c66
Revises: 3ff931743b7e
Create Date: 2026-04-14 20:30:16.710755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcc81d767c66'
down_revision: Union[str, Sequence[str], None] = '3ff931743b7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    column_names = {column['name'] for column in inspector.get_columns('notes')}

    if 'category' not in column_names:
        op.add_column('notes', sa.Column('category', sa.String(length=200), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    column_names = {column['name'] for column in inspector.get_columns('notes')}

    if 'category' in column_names:
        op.drop_column('notes', 'category')

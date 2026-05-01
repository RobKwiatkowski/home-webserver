"""init

Revision ID: 3ff931743b7e
Revises: 
Create Date: 2026-04-14 20:08:37.862151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ff931743b7e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'notes' not in inspector.get_table_names():
        op.create_table('notes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_notes_id'), 'notes', ['id'], unique=False)
        return

    index_names = {index['name'] for index in inspector.get_indexes('notes')}
    if op.f('ix_notes_id') not in index_names:
        op.create_index(op.f('ix_notes_id'), 'notes', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'notes' not in inspector.get_table_names():
        return

    index_names = {index['name'] for index in inspector.get_indexes('notes')}
    if op.f('ix_notes_id') in index_names:
        op.drop_index(op.f('ix_notes_id'), table_name='notes')
    op.drop_table('notes')

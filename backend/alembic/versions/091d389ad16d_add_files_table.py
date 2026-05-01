"""add_files_table

Revision ID: 091d389ad16d
Revises: fcc81d767c66
Create Date: 2026-04-19 09:31:44.550606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '091d389ad16d'
down_revision: Union[str, Sequence[str], None] = 'fcc81d767c66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'files' not in inspector.get_table_names():
        op.create_table('files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_name', sa.String(length=255), nullable=False),
        sa.Column('stored_name', sa.String(length=255), nullable=False),
        sa.Column('content_type', sa.String(length=255), nullable=True),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stored_name')
        )
        op.create_index(op.f('ix_files_id'), 'files', ['id'], unique=False)
        return

    index_names = {index['name'] for index in inspector.get_indexes('files')}
    if op.f('ix_files_id') not in index_names:
        op.create_index(op.f('ix_files_id'), 'files', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'files' not in inspector.get_table_names():
        return

    index_names = {index['name'] for index in inspector.get_indexes('files')}
    if op.f('ix_files_id') in index_names:
        op.drop_index(op.f('ix_files_id'), table_name='files')
    op.drop_table('files')

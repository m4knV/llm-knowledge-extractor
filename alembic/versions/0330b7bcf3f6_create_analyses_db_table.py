"""create_analyses_db_table

Revision ID: 0330b7bcf3f6
Revises: 
Create Date: 2025-09-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0330b7bcf3f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    # Install uuid-ossp extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    op.create_table('analyses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('original_text', sa.Text(), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('topics', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('sentiment', sa.String(length=20), nullable=False),
    sa.Column('keywords', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('confidence_score', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analyses_id'), 'analyses', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_analyses_id'), table_name='analyses')
    op.drop_table('analyses')

"""Add keywords and search topic keywords tables

Revision ID: add_keywords_tables
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_keywords_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create keywords table
    op.create_table('keywords',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('popularity', sa.Float(), nullable=True),
        sa.Column('is_trending', sa.Boolean(), nullable=True),
        sa.Column('topics_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_keywords_id'), 'keywords', ['id'], unique=False)
    op.create_index(op.f('ix_keywords_name'), 'keywords', ['name'], unique=True)

    # Create search_topic_keywords table
    op.create_table('search_topic_keywords',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('search_topic_id', sa.Integer(), nullable=False),
        sa.Column('keyword_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_search_topic_keywords_id'), 'search_topic_keywords', ['id'], unique=False)

    # Add foreign key constraints
    op.create_foreign_key(None, 'search_topic_keywords', 'search_topics', ['search_topic_id'], ['id'])
    op.create_foreign_key(None, 'search_topic_keywords', 'keywords', ['keyword_id'], ['id'])


def downgrade():
    # Drop foreign key constraints
    op.drop_constraint(None, 'search_topic_keywords', type_='foreignkey')
    op.drop_constraint(None, 'search_topic_keywords', type_='foreignkey')

    # Drop tables
    op.drop_index(op.f('ix_search_topic_keywords_id'), table_name='search_topic_keywords')
    op.drop_table('search_topic_keywords')
    op.drop_index(op.f('ix_keywords_name'), table_name='keywords')
    op.drop_index(op.f('ix_keywords_id'), table_name='keywords')
    op.drop_table('keywords')

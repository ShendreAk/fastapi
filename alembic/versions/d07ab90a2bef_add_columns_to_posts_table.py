"""add columns to posts table

Revision ID: d07ab90a2bef
Revises: a2776ae7c251
Create Date: 2024-09-10 18:40:56.623959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd07ab90a2bef'
down_revision: Union[str, None] = 'a2776ae7c251'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'ratings', sa.Integer(), nullable=False, default=0))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'ratings')
    op.drop_column('posts', 'created_at')
    pass

"""add body column to posts table

Revision ID: 8b228b2c5ef0
Revises: 8e2c9308129c
Create Date: 2024-09-10 18:15:39.232920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b228b2c5ef0'
down_revision: Union[str, None] = '8e2c9308129c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('body', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', "body")
    pass

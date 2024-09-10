"""add foreign key to posts table

Revision ID: d1ef6986a583
Revises: d07ab90a2bef
Create Date: 2024-09-10 18:49:58.599612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1ef6986a583'
down_revision: Union[str, None] = 'd07ab90a2bef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts',referent_table='users',local_cols=['user_id'],remote_cols=['id'],ondelete='CASCADE',)
    pass


def downgrade() -> None:
    op.drop_constraint(constraint_name='posts_users_fkey',
    table_name='posts')
    op.drop_column("posts",'user_id')
    pass

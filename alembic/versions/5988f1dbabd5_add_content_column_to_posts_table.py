"""add content column to posts table

Revision ID: 5988f1dbabd5
Revises: 40a68e70dba4
Create Date: 2024-11-15 12:23:47.166157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5988f1dbabd5'
down_revision: Union[str, None] = '40a68e70dba4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

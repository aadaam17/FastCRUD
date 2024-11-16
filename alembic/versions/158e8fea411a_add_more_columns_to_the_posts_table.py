"""add more columns to the posts table

Revision ID: 158e8fea411a
Revises: 444396358879
Create Date: 2024-11-15 12:50:07.997044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '158e8fea411a'
down_revision: Union[str, None] = '444396358879'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'),)
    op.add_column(
        'posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published'),
    op.drop_column('posts', 'created_at')
    pass

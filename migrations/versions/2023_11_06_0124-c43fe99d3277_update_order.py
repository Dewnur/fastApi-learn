"""update order

Revision ID: c43fe99d3277
Revises: 361bb26cf42b
Create Date: 2023-11-06 01:24:22.159904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c43fe99d3277'
down_revision: Union[str, None] = '361bb26cf42b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

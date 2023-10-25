"""add relationship profile to user

Revision ID: 597bdd92b551
Revises: 2b2cb02c83c3
Create Date: 2023-10-25 16:31:02.137362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '597bdd92b551'
down_revision: Union[str, None] = '2b2cb02c83c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('profile_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'order', 'profile', ['profile_id'], ['id'])
    op.add_column('profile', sa.Column('user_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'profile', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profile', type_='foreignkey')
    op.drop_column('profile', 'user_id')
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'profile_id')
    # ### end Alembic commands ###

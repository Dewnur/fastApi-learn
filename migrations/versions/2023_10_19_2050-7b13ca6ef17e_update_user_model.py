"""update user model

Revision ID: 7b13ca6ef17e
Revises: c164ed9e82f0
Create Date: 2023-10-19 20:50:25.728564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7b13ca6ef17e'
down_revision: Union[str, None] = 'c164ed9e82f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'gender',
               existing_type=postgresql.ENUM('female', 'male', 'other', name='igenderenum'),
               nullable=True)
    op.alter_column('user', 'address',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'address',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'gender',
               existing_type=postgresql.ENUM('female', 'male', 'other', name='igenderenum'),
               nullable=False)
    op.alter_column('user', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
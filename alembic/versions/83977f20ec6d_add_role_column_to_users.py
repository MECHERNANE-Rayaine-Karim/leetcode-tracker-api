"""add role column to users

Revision ID: 83977f20ec6d
Revises: e8c1c1e61c8b
Create Date: 2026-07-28 11:16:15.349390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83977f20ec6d'
down_revision: Union[str, Sequence[str], None] = 'e8c1c1e61c8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_enum = sa.Enum('ADMIN', 'REGULAR', name='role')
    role_enum.create(op.get_bind())
    op.add_column('users', sa.Column('role', role_enum, server_default='REGULAR', nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'role')
    sa.Enum(name='role').drop(op.get_bind())
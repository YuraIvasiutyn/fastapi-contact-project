"""Init

Revision ID: 34956da562ea
Revises: 0d0bca7f3dca
Create Date: 2025-05-27 10:46:50.204845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34956da562ea'
down_revision: Union[str, None] = '0d0bca7f3dca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=150), nullable=False))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['username'])
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.VARCHAR(length=150), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'username')
    # ### end Alembic commands ###

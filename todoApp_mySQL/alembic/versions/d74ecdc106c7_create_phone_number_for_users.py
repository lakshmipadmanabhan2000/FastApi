"""Create phone number for users

Revision ID: d74ecdc106c7
Revises: 
Create Date: 2026-04-10 23:33:36.011451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd74ecdc106c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #pass
    op.add_column('users',sa.Column('phone_number',sa.String(20),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    #pass
    op.drop_column("users","phone_number")

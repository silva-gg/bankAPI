"""Add transfer to transaction type enum

Revision ID: add_transfer_enum
Revises: 5cf8bd71bef6
Create Date: 2026-01-03 23:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_transfer_enum'
down_revision: Union[str, None] = '7d75e055f673'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'transfer' value to the existing transactiontype enum
    # PostgreSQL requires using ALTER TYPE ... ADD VALUE
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'transfer'")


def downgrade() -> None:
    # PostgreSQL does not support removing enum values directly
    # If downgrade is needed, the enum would need to be recreated
    # For now, we'll leave it as is since removing enum values is complex
    pass

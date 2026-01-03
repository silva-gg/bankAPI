"""DB Construction 5

Revision ID: 9d86d1626221
Revises: 50e9b6870c4b
Create Date: 2026-01-02 21:52:26.457964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.contrib.models import AccountType


# revision identifiers, used by Alembic.
revision: str = '9d86d1626221'
down_revision: Union[str, None] = '50e9b6870c4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the ENUM type first using values from AccountType enum
    account_type_enum = sa.Enum(*[e.value for e in AccountType], name='accounttype')
    account_type_enum.create(op.get_bind(), checkfirst=True)

    # Now alter the column to use the ENUM type
    op.alter_column('accounts', 'account_type',
               existing_type=sa.VARCHAR(length=50),
               type_=account_type_enum,
               existing_comment='Account type',
               existing_nullable=False,
               postgresql_using='account_type::accounttype')

    # ### end Alembic commands ###


def downgrade() -> None:
    # Revert column to VARCHAR
    op.alter_column('accounts', 'account_type',
               existing_type=sa.Enum(*[e.value for e in AccountType], name='accounttype'),
               type_=sa.VARCHAR(length=50),
               existing_comment='Account type',
               existing_nullable=False)
    
    # Drop the ENUM type
    sa.Enum(name='accounttype').drop(op.get_bind(), checkfirst=True)

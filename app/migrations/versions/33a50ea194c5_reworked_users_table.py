"""reworked users table

Revision ID: 33a50ea194c5
Revises: 4598d89b9626
Create Date: 2025-04-29 13:17:16.399724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33a50ea194c5'
down_revision: Union[str, None] = '4598d89b9626'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_first_name_key', 'users', type_='unique')
    op.drop_constraint('users_last_name_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_last_name_key', 'users', ['last_name'])
    op.create_unique_constraint('users_first_name_key', 'users', ['first_name'])
    # ### end Alembic commands ###

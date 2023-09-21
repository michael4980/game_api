"""init_tables

Revision ID: 98e96c0b0324
Revises: 
Create Date: 2023-09-19 18:14:56.671944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "98e96c0b0324"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", mysql.BIGINT(unsigned=True), nullable=False, auto_increment=True, primary_key=True),
        sa.Column("name", sa.VARCHAR(255), nullable=False),
        sa.Column("points", mysql.INTEGER()),
    )

    op.create_table(
        "items",
        sa.Column("id", mysql.BIGINT(unsigned=True), nullable=False, auto_increment=True, primary_key=True),
        sa.Column("name", sa.VARCHAR(255), nullable=False),
        sa.Column("price", mysql.INTEGER()),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("items")

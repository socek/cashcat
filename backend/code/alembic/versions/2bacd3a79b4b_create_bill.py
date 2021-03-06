"""create bill

Revision ID: 2bacd3a79b4b
Revises: 2c5d40778b47
Create Date: 2018-10-18 10:26:56.427737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2bacd3a79b4b"
down_revision = "2c5d40778b47"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bills",
        sa.Column("uid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("place", sa.String(), nullable=True),
        sa.Column("billed_at", sa.String(), nullable=False),
        sa.Column("wallet_uid", postgresql.UUID(as_uuid=False), nullable=False),
        sa.ForeignKeyConstraint(
            ["wallet_uid"], ["wallets.uid"], name=op.f("fk_bills_wallet_uid_wallets")
        ),
        sa.PrimaryKeyConstraint("uid", name=op.f("pk_bills")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("bills")
    # ### end Alembic commands ###

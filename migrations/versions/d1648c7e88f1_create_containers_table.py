"""create containers table

Revision ID: d1648c7e88f1
Create Date: 2022-05-01 19:23:56.411242

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d1648c7e88f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "containers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "type",
            sa.Enum("BASIC", "REFRIGERATED", "TWO_FLOOR", "HALF"),
            nullable=False,
        ),
        sa.Column("volume", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table("containers")

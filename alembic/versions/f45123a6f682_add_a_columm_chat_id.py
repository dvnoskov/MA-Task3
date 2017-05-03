"""add a columm chat.id

Revision ID: f45123a6f682
Revises: cc9be778ee39
Create Date: 2017-04-24 22:19:47.756577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f45123a6f682'
down_revision = 'cc9be778ee39'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user',sa.Column('chat_id',sa.String(10)))
    pass


def downgrade():
    pass

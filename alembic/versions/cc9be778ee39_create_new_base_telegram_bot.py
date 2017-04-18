"""create new base telegram_bot

Revision ID: cc9be778ee39
Revises: 
Create Date: 2017-03-25 20:56:55.426029

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy_utils import JSONType
from sqlalchemy_utils import EmailType



# revision identifiers, used by Alembic.
revision = 'cc9be778ee39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('buy',
                    sa.Column('buy_id', sa.Integer),
                    sa.Column('id_user', sa.Integer),
                    sa.Column('phone', sa.String(20)),
                    sa.Column('adress_city', sa.String(60)),
                    sa.Column('data_time_city', sa.String(40)),
                    sa.Column('menu', sa.String(60)),
                    sa.Column('total',sa.Float),
                    sa.Column('calendar', sa.Boolean, default=False),
                    sa.Column('created_on', sa.DateTime(timezone=True), default=datetime.utcnow),
                    sa.Column('temp', sa.String(20)),
                    sa.PrimaryKeyConstraint('buy_id')

                    )


    op.create_table('user',
                    sa.Column('user_id', sa.Integer),
                    sa.Column('username', sa.String(15)),
                    sa.Column('email_address', EmailType),
                    sa.Column('token', JSONType),
                    sa.Column('created_on', sa.DateTime(timezone=True), default=datetime.utcnow),
                    sa.Column('updated_on', sa.DateTime(timezone=True),  default=datetime.now, onupdate=datetime.utcnow),
                    sa.PrimaryKeyConstraint('user_id')

                    )

def downgrade():
    op.drop_table('buy')
    op.drop_table('user')
    pass


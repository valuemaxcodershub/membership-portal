"""changed about to business_about

Revision ID: b2fb838ddf35
Revises: 
Create Date: 2022-10-18 13:12:52.198782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2fb838ddf35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('business_about', sa.String(), nullable=True))
    op.drop_column('user', 'about')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about', sa.VARCHAR(), nullable=True))
    op.drop_column('user', 'business_about')
    # ### end Alembic commands ###

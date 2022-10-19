"""Business profile variables

Revision ID: bc44eddcc0c3
Revises: b2fb838ddf35
Create Date: 2022-10-18 13:42:16.759720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc44eddcc0c3'
down_revision = 'b2fb838ddf35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('business_services', sa.String(), nullable=True))
    op.add_column('user', sa.Column('business_images', sa.String(), nullable=True))
    op.add_column('user', sa.Column('business_facebook', sa.String(), nullable=True))
    op.add_column('user', sa.Column('business_twitter', sa.String(), nullable=True))
    op.add_column('user', sa.Column('business_linkedin', sa.String(), nullable=True))
    op.add_column('user', sa.Column('business_whatsapp', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'business_whatsapp')
    op.drop_column('user', 'business_linkedin')
    op.drop_column('user', 'business_twitter')
    op.drop_column('user', 'business_facebook')
    op.drop_column('user', 'business_images')
    op.drop_column('user', 'business_services')
    # ### end Alembic commands ###
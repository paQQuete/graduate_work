"""Funds on hold added

Revision ID: 1c15be0c8f60
Revises: 9d7ee5145829
Create Date: 2023-05-20 20:30:08.053457

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1c15be0c8f60'
down_revision = '9d7ee5145829'
branch_labels = None
depends_on = '9d7ee5145829'


def upgrade() -> None:
    op.create_table('funds_hold',
                    sa.Column('type', sa.Enum('spending', 'refund', name='typesenumholds'), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('cost', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index(op.f('ix_billing_funds_hold_type'), 'funds_hold', ['type'], unique=False, schema='billing')
    op.create_index(op.f('ix_billing_funds_hold_user_uuid'), 'funds_hold', ['user_uuid'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_funds_hold_uuid'), 'funds_hold', ['uuid'], unique=False, schema='billing')


def downgrade() -> None:
    op.drop_index(op.f('ix_billing_funds_hold_uuid'), table_name='funds_hold', schema='billing')
    op.drop_index(op.f('ix_billing_funds_hold_user_uuid'), table_name='funds_hold', schema='billing')
    op.drop_index(op.f('ix_billing_funds_hold_type'), table_name='funds_hold', schema='billing')
    op.drop_table('funds_hold', schema='billing')

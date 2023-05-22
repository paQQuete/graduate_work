"""trans order

Revision ID: a214819c2036
Revises: 1c15be0c8f60
Create Date: 2023-05-22 11:07:11.117375

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a214819c2036'
down_revision = '1c15be0c8f60'
branch_labels = None
depends_on = '1c15be0c8f60'


def upgrade() -> None:
    op.create_table('trans_order',
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('payment_session_id', sa.String(), nullable=False),
                    sa.Column('subscribe_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('started_at', sa.DateTime(), nullable=False),
                    sa.Column('ended_at', sa.DateTime(), nullable=True),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index(op.f('ix_billing_trans_order_payment_session_id'), 'trans_order', ['payment_session_id'],
                    unique=False, schema='billing')
    op.create_index(op.f('ix_billing_trans_order_subscribe_id'), 'trans_order', ['subscribe_id'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_trans_order_user_uuid'), 'trans_order', ['user_uuid'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_trans_order_uuid'), 'trans_order', ['uuid'], unique=False, schema='billing')


def downgrade() -> None:
    op.drop_index(op.f('ix_billing_trans_order_uuid'), table_name='trans_order', schema='billing')
    op.drop_index(op.f('ix_billing_trans_order_user_uuid'), table_name='trans_order', schema='billing')
    op.drop_index(op.f('ix_billing_trans_order_subscribe_id'), table_name='trans_order', schema='billing')
    op.drop_index(op.f('ix_billing_trans_order_payment_session_id'), table_name='trans_order', schema='billing')
    op.drop_table('trans_order', schema='billing')

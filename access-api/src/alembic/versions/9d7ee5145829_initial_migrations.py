"""initial migrations

Revision ID: 9d7ee5145829
Revises: 
Create Date: 2023-05-18 21:53:03.194960

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9d7ee5145829'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE SCHEMA if not exists billing;""")
    op.create_table('balance',
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('balance', sa.Integer(), nullable=False),
                    sa.Column('timestamp_offset', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index(op.f('ix_billing_balance_user_uuid'), 'balance', ['user_uuid'], unique=False, schema='billing')
    op.create_index(op.f('ix_billing_balance_uuid'), 'balance', ['uuid'], unique=False, schema='billing')
    op.create_table('transaction',
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('type', sa.Enum('topup', 'spending', 'refund', name='typesenum'), nullable=False),
                    sa.Column('cost', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index(op.f('ix_billing_transaction_type'), 'transaction', ['type'], unique=False, schema='billing')
    op.create_index(op.f('ix_billing_transaction_user_uuid'), 'transaction', ['user_uuid'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_transaction_uuid'), 'transaction', ['uuid'], unique=False, schema='billing')


def downgrade() -> None:
    op.drop_index(op.f('ix_billing_transaction_uuid'), table_name='transaction', schema='billing')
    op.drop_index(op.f('ix_billing_transaction_user_uuid'), table_name='transaction', schema='billing')
    op.drop_index(op.f('ix_billing_transaction_type'), table_name='transaction', schema='billing')
    op.drop_table('transaction', schema='billing')
    op.drop_index(op.f('ix_billing_balance_uuid'), table_name='balance', schema='billing')
    op.drop_index(op.f('ix_billing_balance_user_uuid'), table_name='balance', schema='billing')
    op.drop_table('balance', schema='billing')

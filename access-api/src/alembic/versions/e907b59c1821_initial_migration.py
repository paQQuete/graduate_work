"""initial_migration

Revision ID: e907b59c1821
Revises: 
Create Date: 2023-06-01 23:34:26.104309

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e907b59c1821'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS billing;')
    op.create_table('balance',
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('balance', sa.Integer(), nullable=False),
                    sa.Column('timestamp_offset', sa.DateTime(), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index(op.f('ix_billing_balance_user_uuid'), 'balance', ['user_uuid'], unique=False, schema='billing')
    op.create_index(op.f('ix_billing_balance_uuid'), 'balance', ['uuid'], unique=False, schema='billing')
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
    op.create_table('transaction',
                    sa.Column('type', sa.Enum('topup', 'spending', 'refund', name='typesenum'), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('cost', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index(op.f('ix_billing_transaction_type'), 'transaction', ['type'], unique=False, schema='billing')
    op.create_index(op.f('ix_billing_transaction_user_uuid'), 'transaction', ['user_uuid'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_transaction_uuid'), 'transaction', ['uuid'], unique=False, schema='billing')
    op.create_table('granted_access',
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('subscription_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
                    sa.Column('granted_at', sa.DateTime(), nullable=False),
                    sa.Column('available_until', sa.DateTime(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['subscription_id'], ['content.subscribe.id'], ),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index(op.f('ix_billing_granted_access_user_uuid'), 'granted_access', ['user_uuid'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_granted_access_uuid'), 'granted_access', ['uuid'], unique=False, schema='billing')
    op.create_table('granted_films',
                    sa.Column('movie_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('granted_at', sa.DateTime(), nullable=False),
                    sa.Column('grant_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['grant_uuid'], ['billing.granted_access.uuid'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='billing'
                    )
    op.create_index('ix_billing_granted_films_movie_user_uuids', 'granted_films', ['movie_uuid', 'user_uuid'],
                    unique=False, schema='billing')
    op.create_index(op.f('ix_billing_granted_films_movie_uuid'), 'granted_films', ['movie_uuid'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_granted_films_user_uuid'), 'granted_films', ['user_uuid'], unique=False,
                    schema='billing')
    op.create_index(op.f('ix_billing_granted_films_uuid'), 'granted_films', ['uuid'], unique=False, schema='billing')


def downgrade() -> None:
    op.drop_index(op.f('ix_billing_granted_films_uuid'), table_name='granted_films', schema='billing')
    op.drop_index(op.f('ix_billing_granted_films_user_uuid'), table_name='granted_films', schema='billing')
    op.drop_index(op.f('ix_billing_granted_films_movie_uuid'), table_name='granted_films', schema='billing')
    op.drop_index('ix_billing_granted_films_movie_user_uuids', table_name='granted_films', schema='billing')
    op.drop_table('granted_films', schema='billing')
    op.drop_index(op.f('ix_billing_granted_access_uuid'), table_name='granted_access', schema='billing')
    op.drop_index(op.f('ix_billing_granted_access_user_uuid'), table_name='granted_access', schema='billing')
    op.drop_table('granted_access', schema='billing')
    op.drop_index(op.f('ix_billing_transaction_uuid'), table_name='transaction', schema='billing')
    op.drop_index(op.f('ix_billing_transaction_user_uuid'), table_name='transaction', schema='billing')
    op.drop_index(op.f('ix_billing_transaction_type'), table_name='transaction', schema='billing')
    op.drop_table('transaction', schema='billing')
    op.drop_index(op.f('ix_billing_trans_order_uuid'), table_name='trans_order', schema='billing')
    op.drop_index(op.f('ix_billing_trans_order_user_uuid'), table_name='trans_order', schema='billing')
    op.drop_index(op.f('ix_billing_trans_order_subscribe_id'), table_name='trans_order', schema='billing')
    op.drop_index(op.f('ix_billing_trans_order_payment_session_id'), table_name='trans_order', schema='billing')
    op.drop_table('trans_order', schema='billing')
    op.drop_index(op.f('ix_billing_funds_hold_uuid'), table_name='funds_hold', schema='billing')
    op.drop_index(op.f('ix_billing_funds_hold_user_uuid'), table_name='funds_hold', schema='billing')
    op.drop_index(op.f('ix_billing_funds_hold_type'), table_name='funds_hold', schema='billing')
    op.drop_table('funds_hold', schema='billing')
    op.drop_index(op.f('ix_billing_balance_uuid'), table_name='balance', schema='billing')
    op.drop_index(op.f('ix_billing_balance_user_uuid'), table_name='balance', schema='billing')
    op.drop_table('balance', schema='billing')

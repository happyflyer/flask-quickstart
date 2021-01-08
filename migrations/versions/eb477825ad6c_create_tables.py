from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb477825ad6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sys_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('permission', sa.String(length=32), nullable=True),
    sa.Column('last_visit', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sys_user_token'), 'sys_user', ['token'], unique=True)
    op.create_index(op.f('ix_sys_user_username'), 'sys_user', ['username'], unique=True)
    op.create_table('sys_visit_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('method', sa.String(length=10), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('scheme', sa.String(length=10), nullable=True),
    sa.Column('host', sa.String(length=20), nullable=True),
    sa.Column('path', sa.String(length=50), nullable=True),
    sa.Column('query_string', sa.String(length=100), nullable=True),
    sa.Column('json', sa.String(length=200), nullable=True),
    sa.Column('blueprint', sa.String(length=20), nullable=True),
    sa.Column('endpoint', sa.String(length=50), nullable=True),
    sa.Column('remote_addr', sa.String(length=20), nullable=True),
    sa.Column('user_agent', sa.String(length=200), nullable=True),
    sa.Column('status_code', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['sys_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sys_visit_log')
    op.drop_index(op.f('ix_sys_user_username'), table_name='sys_user')
    op.drop_index(op.f('ix_sys_user_token'), table_name='sys_user')
    op.drop_table('sys_user')
    # ### end Alembic commands ###
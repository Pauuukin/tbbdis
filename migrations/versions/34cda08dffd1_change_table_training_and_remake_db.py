"""change table training and remake db

Revision ID: 34cda08dffd1
Revises: 
Create Date: 2019-06-05 21:29:05.043808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34cda08dffd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('training',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_training', sa.String(length=256), nullable=True),
    sa.Column('tipe', sa.String(length=256), nullable=True),
    sa.Column('muscle_group', sa.String(length=256), nullable=True),
    sa.Column('gender', sa.String(length=32), nullable=True),
    sa.Column('count_day', sa.Integer(), nullable=True),
    sa.Column('name_sport', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_name_training'), 'training', ['name_training'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('dateOfBirth', sa.Date(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('full_name', sa.String(length=128), nullable=True),
    sa.Column('gender', sa.String(length=32), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_exercises', sa.String(length=256), nullable=True),
    sa.Column('rules', sa.Text(length=500), nullable=True),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('training_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['training_id'], ['training.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercises_name_exercises'), 'exercises', ['name_exercises'], unique=False)
    op.create_index(op.f('ix_exercises_rules'), 'exercises', ['rules'], unique=False)
    op.create_table('training_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=True),
    sa.Column('date_finish', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('training_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['training_id'], ['training.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_list_date_start'), 'training_list', ['date_start'], unique=False)
    op.create_table('info_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('arms', sa.Integer(), nullable=True),
    sa.Column('chest', sa.Integer(), nullable=True),
    sa.Column('waist', sa.Integer(), nullable=True),
    sa.Column('femur', sa.Integer(), nullable=True),
    sa.Column('heartDiseases', sa.String(length=12), nullable=True),
    sa.Column('date_of_change', sa.Date(), nullable=True),
    sa.Column('training_list_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['training_list_id'], ['training_list.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('info_user')
    op.drop_index(op.f('ix_training_list_date_start'), table_name='training_list')
    op.drop_table('training_list')
    op.drop_index(op.f('ix_exercises_rules'), table_name='exercises')
    op.drop_index(op.f('ix_exercises_name_exercises'), table_name='exercises')
    op.drop_table('exercises')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_training_name_training'), table_name='training')
    op.drop_table('training')
    # ### end Alembic commands ###

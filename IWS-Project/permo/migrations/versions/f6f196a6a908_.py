"""empty message

Revision ID: f6f196a6a908
Revises: 98a80b3266d4
Create Date: 2022-11-30 23:28:22.546159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6f196a6a908'
down_revision = '98a80b3266d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission_numbers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('permission_number', sa.Integer(), nullable=True),
    sa.Column('assigned', sa.Boolean(), nullable=True),
    sa.Column('course_name', sa.String(), nullable=True),
    sa.Column('professor_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('permission_numbers', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_permission_numbers_assigned'), ['assigned'], unique=False)
        batch_op.create_index(batch_op.f('ix_permission_numbers_course_name'), ['course_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_permission_numbers_permission_number'), ['permission_number'], unique=False)
        batch_op.create_index(batch_op.f('ix_permission_numbers_professor_id'), ['professor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_permission_numbers_student_id'), ['student_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permission_numbers', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_permission_numbers_student_id'))
        batch_op.drop_index(batch_op.f('ix_permission_numbers_professor_id'))
        batch_op.drop_index(batch_op.f('ix_permission_numbers_permission_number'))
        batch_op.drop_index(batch_op.f('ix_permission_numbers_course_name'))
        batch_op.drop_index(batch_op.f('ix_permission_numbers_assigned'))

    op.drop_table('permission_numbers')
    # ### end Alembic commands ###

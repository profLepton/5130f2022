"""empty message

Revision ID: 2af48785fa47
Revises: a3dd775f7ab5
Create Date: 2022-11-29 13:28:21.887733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2af48785fa47'
down_revision = 'a3dd775f7ab5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('professr_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('class_name', sa.String(length=64), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('professor_id', sa.Integer(), nullable=True),
    sa.Column('permission_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['professor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('professr_requests', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_professr_requests_class_name'), ['class_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_professr_requests_professor_id'), ['professor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_professr_requests_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_professr_requests_student_id'), ['student_id'], unique=False)

    op.create_table('student_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('class_name', sa.String(length=64), nullable=True),
    sa.Column('professor_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('permission_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('student_requests', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_student_requests_class_name'), ['class_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_student_requests_professor_id'), ['professor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_student_requests_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_student_requests_student_id'), ['student_id'], unique=False)

    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.drop_index('ix_requests_course_id')
        batch_op.drop_index('ix_requests_status')
        batch_op.drop_index('ix_requests_student_id')

    op.drop_table('requests')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.BOOLEAN(), nullable=True),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.Column('course_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['college_course.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.create_index('ix_requests_student_id', ['student_id'], unique=False)
        batch_op.create_index('ix_requests_status', ['status'], unique=False)
        batch_op.create_index('ix_requests_course_id', ['course_id'], unique=False)

    with op.batch_alter_table('student_requests', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_student_requests_student_id'))
        batch_op.drop_index(batch_op.f('ix_student_requests_status'))
        batch_op.drop_index(batch_op.f('ix_student_requests_professor_id'))
        batch_op.drop_index(batch_op.f('ix_student_requests_class_name'))

    op.drop_table('student_requests')
    with op.batch_alter_table('professr_requests', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_professr_requests_student_id'))
        batch_op.drop_index(batch_op.f('ix_professr_requests_status'))
        batch_op.drop_index(batch_op.f('ix_professr_requests_professor_id'))
        batch_op.drop_index(batch_op.f('ix_professr_requests_class_name'))

    op.drop_table('professr_requests')
    # ### end Alembic commands ###
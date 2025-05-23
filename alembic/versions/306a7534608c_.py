"""empty message

Revision ID: 306a7534608c
Revises: 616d0f3aa9fc
Create Date: 2025-04-06 17:17:02.211104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '306a7534608c'
down_revision = '616d0f3aa9fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('school', sa.Column('image_url', sa.String(), nullable=True))
    op.add_column('school', sa.Column('description', sa.String(), nullable=True))
    op.alter_column('school', 'types',
               existing_type=sa.JSON(),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=True)
    op.drop_index('ix_school_id', table_name='school', postgresql_using='prefix')
    op.create_index(op.f('ix_school_id'), 'school', ['id'], unique=False)
    op.drop_index('ix_school_school_unit_code', table_name='school', postgresql_using='prefix')
    op.create_index(op.f('ix_school_school_unit_code'), 'school', ['school_unit_code'], unique=False)
    op.drop_index('ix_school_types', table_name='school', postgresql_using='prefix')
    op.create_index(op.f('ix_school_types'), 'school', ['types'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_school_types'), table_name='school')
    op.create_index('ix_school_types', 'school', [sa.text('types NULLS FIRST')], unique=False, postgresql_using='prefix')
    op.drop_index(op.f('ix_school_school_unit_code'), table_name='school')
    op.create_index('ix_school_school_unit_code', 'school', [sa.text('school_unit_code NULLS FIRST')], unique=False, postgresql_using='prefix')
    op.drop_index(op.f('ix_school_id'), table_name='school')
    op.create_index('ix_school_id', 'school', [sa.text('id NULLS FIRST')], unique=False, postgresql_using='prefix')
    op.alter_column('school', 'types',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=sa.JSON(),
               existing_nullable=True)
    op.drop_column('school', 'description')
    op.drop_column('school', 'image_url')
    # ### end Alembic commands ###

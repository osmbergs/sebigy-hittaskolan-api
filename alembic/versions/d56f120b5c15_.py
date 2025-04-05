"""empty message

Revision ID: d56f120b5c15
Revises: 
Create Date: 2025-04-05 16:47:04.904788

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd56f120b5c15'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('school',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('types', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('school_unit_code', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('headmaster', sa.String(), nullable=False),
    sa.Column('municipality_code', sa.String(), nullable=False),
    sa.Column('visit_address_street', sa.String(), nullable=False),
    sa.Column('visit_address_postal_code', sa.String(), nullable=False),
    sa.Column('visit_address_locality', sa.String(), nullable=False),
    sa.Column('geo_lat', sa.String(), nullable=False),
    sa.Column('geo_long', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_school_id'), 'school', ['id'], unique=False)
    op.create_index(op.f('ix_school_school_unit_code'), 'school', ['school_unit_code'], unique=False)
    op.create_index(op.f('ix_school_types'), 'school', ['types'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_school_types'), table_name='school')
    op.drop_index(op.f('ix_school_school_unit_code'), table_name='school')
    op.drop_index(op.f('ix_school_id'), table_name='school')
    op.drop_table('school')
    # ### end Alembic commands ###

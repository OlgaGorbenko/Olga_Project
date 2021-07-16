"""empty message

Revision ID: 30c30592a2d6
Revises: 
Create Date: 2021-07-16 21:31:23.695809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30c30592a2d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('type_of_product', sa.String(length=120), nullable=True),
    sa.Column('unit_of_measure', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_title'), ['title'], unique=True)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recipe_title'), ['title'], unique=True)

    op.create_table('shopping_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('unit_of_measure', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shopping_list_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shopping_list_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('unit_of_measure', sa.String(length=120), nullable=True),
    sa.Column('is_buyed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['shopping_list_id'], ['shopping_list.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shopping_list_item')
    op.drop_table('ingredient')
    op.drop_table('shopping_list')
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recipe_title'))

    op.drop_table('recipe')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_title'))

    op.drop_table('product')
    # ### end Alembic commands ###
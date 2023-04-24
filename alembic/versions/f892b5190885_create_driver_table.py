"""Create Driver table

Revision ID: f892b5190885
Revises: 
Create Date: 2023-04-24 00:29:39.556310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f892b5190885'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("Driver",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("name",sa.String(),nullable=False)
                    
                    )
    
    
    
    pass


def downgrade() :
    op.drop_table("Driver")
    
    
    pass

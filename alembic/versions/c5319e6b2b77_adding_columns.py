"""adding columns

Revision ID: c5319e6b2b77
Revises: f892b5190885
Create Date: 2023-04-24 00:49:07.783312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5319e6b2b77'
down_revision = 'f892b5190885'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column("Driver",sa.Column("email",sa.String(),nullable=False)),
    op.add_column("Driver",sa.Column("password",sa.String(),nullable=False))
    
    


def downgrade()  :
    op.drop_column("Driver","email"),
    op.drop_column("Driver","password")
    

"""added a foreign key

Revision ID: d121974f6248
Revises: d445248c9e87
Create Date: 2025-05-08 13:58:59.083995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd121974f6248'
down_revision: Union[str, None] = 'd445248c9e87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'posts',
        sa.Column(
            'owner_id',
            sa.Integer(),nullable=True
        )
    )

    op.create_foreign_key(
        'posts_users_fk',
        'posts',
        'users',
        ['owner_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_index('ix_post_owner_id', 'posts', ['owner_id'])


def downgrade() -> None:
    # 1. Drop the foreign key first
    op.drop_constraint('fk_post_owner_id', 'post', type_='foreignkey')
    
    # 2. Drop the index (if created)
    op.drop_index('ix_post_owner_id', 'post')
    
    # 3. Finally, drop the column
    op.drop_column('post', 'owner_id')
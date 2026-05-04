"""Add todo is_active column."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260504_02"
down_revision: str | None = "20260504_01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add soft-deactivation support for todos."""
    op.add_column(
        "todos",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.create_index(op.f("ix_todos_is_active"), "todos", ["is_active"], unique=False)


def downgrade() -> None:
    """Remove soft-deactivation support for todos."""
    op.drop_index(op.f("ix_todos_is_active"), table_name="todos")
    op.drop_column("todos", "is_active")

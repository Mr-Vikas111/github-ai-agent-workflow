"""Create todos table."""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260504_01"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply the initial todo schema."""
    op.create_table(
        "todos",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_todos")),
    )
    op.create_index(op.f("ix_todos_created_at"), "todos", ["created_at"], unique=False)
    op.create_index(op.f("ix_todos_is_completed"), "todos", ["is_completed"], unique=False)


def downgrade() -> None:
    """Revert the initial todo schema."""
    op.drop_index(op.f("ix_todos_is_completed"), table_name="todos")
    op.drop_index(op.f("ix_todos_created_at"), table_name="todos")
    op.drop_table("todos")

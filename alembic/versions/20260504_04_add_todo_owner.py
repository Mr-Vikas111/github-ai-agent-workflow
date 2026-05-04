"""Add todo owner association."""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260504_04"
down_revision: str | None = "20260504_03"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Associate todos with users for protected access."""
    op.add_column(
        "todos",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index(op.f("ix_todos_owner_id"), "todos", ["owner_id"], unique=False)
    op.create_foreign_key(
        op.f("fk_todos_owner_id_users"),
        "todos",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Remove todo ownership."""
    op.drop_constraint(op.f("fk_todos_owner_id_users"), "todos", type_="foreignkey")
    op.drop_index(op.f("ix_todos_owner_id"), table_name="todos")
    op.drop_column("todos", "owner_id")

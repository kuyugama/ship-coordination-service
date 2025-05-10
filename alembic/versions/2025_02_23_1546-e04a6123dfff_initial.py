"""Initial

Revision ID: e04a6123dfff
Revises:
Create Date: 2025-02-23 15:46:07.599018

"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e04a6123dfff"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "service_users",
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("login_at", sa.DateTime(), nullable=False),
        sa.Column("active_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_service_users_created_at"), "service_users", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_service_users_id"), "service_users", ["id"], unique=False)
    op.create_index(op.f("ix_service_users_nickname"), "service_users", ["nickname"], unique=False)
    op.create_index(
        op.f("ix_service_users_updated_at"), "service_users", ["updated_at"], unique=False
    )
    op.create_table(
        "service_tokens",
        sa.Column("body", sa.String(), nullable=False),
        sa.Column("owner_id", sa.BIGINT(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["service_users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_service_tokens_body"), "service_tokens", ["body"], unique=True)
    op.create_index(
        op.f("ix_service_tokens_created_at"), "service_tokens", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_service_tokens_id"), "service_tokens", ["id"], unique=False)
    op.create_index(
        op.f("ix_service_tokens_updated_at"), "service_tokens", ["updated_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_service_tokens_updated_at"), table_name="service_tokens")
    op.drop_index(op.f("ix_service_tokens_id"), table_name="service_tokens")
    op.drop_index(op.f("ix_service_tokens_created_at"), table_name="service_tokens")
    op.drop_index(op.f("ix_service_tokens_body"), table_name="service_tokens")
    op.drop_table("service_tokens")
    op.drop_index(op.f("ix_service_users_updated_at"), table_name="service_users")
    op.drop_index(op.f("ix_service_users_nickname"), table_name="service_users")
    op.drop_index(op.f("ix_service_users_id"), table_name="service_users")
    op.drop_index(op.f("ix_service_users_created_at"), table_name="service_users")
    op.drop_table("service_users")

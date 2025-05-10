from datetime import datetime, timedelta

from sqlalchemy import orm

from .. import util
from .base import Base


class User(Base, table="service_users"):
    nickname: orm.Mapped[str] = orm.mapped_column(index=True)
    password_hash: orm.Mapped[str]

    login_at: orm.Mapped[datetime] = orm.mapped_column(default=util.datetime.now)
    active_at: orm.Mapped[datetime] = orm.mapped_column(default=util.datetime.now)

    # Reset updated_at column to tell SQLAlchemy to not update it whenever flush occurs
    # This field should be updated manually
    # to contain date of the reasonable columns(such as nickname or password_hash) only
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=None, nullable=True, index=True)

    @property
    def online(self) -> bool:
        return self.active_at + timedelta(seconds=util.user_active_for()) > util.datetime.now()

    def update_active_at(self) -> None:
        self.active_at = util.datetime.now()

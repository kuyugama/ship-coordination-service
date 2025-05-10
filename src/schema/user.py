from .model import Object, Field, datetime_pd


class User(Object):
    nickname: str = Field(description="User nickname")

    last_login: datetime_pd = Field(description="User last login date", validation_alias="login_at")
    last_active: datetime_pd = Field(
        description="User last login date", validation_alias="active_at"
    )

    online: bool = Field(description="User online status")

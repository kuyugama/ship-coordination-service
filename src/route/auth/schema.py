from src.schema.model import Schema, Field


class SignupSchema(Schema):
    nickname: str = Field(
        min_length=3, max_length=32, pattern="[a-zA-Z0-9_]+", description="Nickname"
    )
    password: str = Field(min_length=8, max_length=64, description="Password")


class SigninSchema(Schema):
    nickname: str = Field(description="Nickname")
    password: str = Field(min_length=8, max_length=64, description="Password")

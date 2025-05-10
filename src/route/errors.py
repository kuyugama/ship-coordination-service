from src.error import define_error

token_invalid = define_error("auth", "invalid-token", "Invalid token", 401)
token_expired = define_error("auth", "token-expired", "Token expired", 403)

user_not_found = define_error("user", "not-found", "User not found", 404)

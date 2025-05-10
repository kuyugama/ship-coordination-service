from src.error import define_error_category

define_error = define_error_category("auth")

already_exists = define_error("user-already-exists", "User already exists", status_code=400)

invalid_password = define_error("invalid-password", "Invalid password", status_code=403)

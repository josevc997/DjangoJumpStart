from PIL import Image


def validate_create_user_form(data):
    errors = {}
    print(data)
    if data.get("email") is None or data.get("email") == "":
        errors["email"] = "Email is required."
    if data.get("password") is None or data.get("password") == "":
        errors["password"] = "Password is required."
    if data.get("username") is None or data.get("username") == "":
        errors["username"] = "Username is required."
    if data.get("first_name") is None or data.get("first_name") == "":
        errors["first_name"] = "First name is required."
    if data.get("last_name") is None or data.get("last_name") == "":
        errors["last_name"] = "Last name is required."
    if data.get("image") is not None:
        try:
            Image.open(data.get("image"))
        except (IOError, OSError):
            errors["image"] = "Invalid image format."
    return errors


def validate_admin_update_user(data):
    errors = {}

    if data.get("first_name") is None or data.get("first_name") == "":
        errors["first_name"] = "First name is required."
    if data.get("last_name") is None or data.get("last_name") == "":
        errors["last_name"] = "Last name is required."
    if data.get("image") is not None:
        try:
            Image.open(data.get("image"))
        except (IOError, OSError):
            errors["image"] = "Invalid image format."
    return errors

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from src.database import (

    create_user,

    get_user_by_email,

    get_user_by_id

)


def register_user(

    username,
    email,
    password

):

    existing_user = (
        get_user_by_email(
            email
        )
    )

    if existing_user:

        return {

            "success": False,

            "message":
            "Email already exists"

        }

    hashed_password = (
        generate_password_hash(
            password
        )
    )

    create_user(

        username,

        email,

        hashed_password

    )

    return {

        "success": True,

        "message":
        "Registration successful"

    }


def login_user(

    email,
    password

):

    user = (
        get_user_by_email(
            email
        )
    )

    if not user:

        return {

            "success": False,

            "message":
            "User not found"

        }

    if not check_password_hash(

        user["password"],

        password

    ):

        return {

            "success": False,

            "message":
            "Invalid password"

        }

    return {

        "success": True,

        "user_id":
        user["id"],

        "username":
        user["username"],

        "email":
        user["email"]

    }


def get_current_user(
    user_id
):

    user = (
        get_user_by_id(
            user_id
        )
    )

    if not user:

        return None

    return {

        "id":
        user["id"],

        "username":
        user["username"],

        "email":
        user["email"]

    }


def verify_password(

    email,

    password

):

    user = (
        get_user_by_email(
            email
        )
    )

    if not user:

        return False

    return check_password_hash(

        user["password"],

        password

    )
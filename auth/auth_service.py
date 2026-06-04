from database.mongodb import users_collection

def authenticate_user(
    username,
    password
):

    user = users_collection.find_one(
        {
            "username": username,
            "password": password
        }
    )

    return user
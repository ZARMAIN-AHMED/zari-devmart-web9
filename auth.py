
import json
import os
from models.user import User

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        data = json.load(f)
        return {email: User(**info) for email, info in data.items()}


def save_users(users):
    data = {email: user.__dict__ for email, user in users.items()}
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)

users_db = load_users()

def login(email, password):
    user = users_db.get(email)
    if user and user.password == password:
        return user
    return None

def register(name, email, password):
    if email in users_db:
        return None
    new_user = User(name, email, password)
    users_db[email] = new_user
    save_users(users_db)
    return new_user

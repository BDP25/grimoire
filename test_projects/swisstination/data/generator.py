"""
Generates passwords for the mock users
"""

import json

import bcrypt

SALT: bytes = b"$2b$12$3kPXS3K7eJN3.tSane82Oe"

# Load the mock users
with open("data/users.json", encoding="utf-8") as f:
    users = json.load(f)

# Generate and set password
for user in users["nodes"]:
    password = user["username"]  # Using the username as the password
    user["password"] = bcrypt.hashpw(password.encode(), SALT).decode("utf-8")

# Save the mock users
with open("data/users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=4)

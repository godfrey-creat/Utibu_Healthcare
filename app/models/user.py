from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): Primary key for the User table.
        username (str): User's username (limited to 64 characters) which is unique.
        password_hash (str): Hashed password (limited to 128 characters).
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        """
        Sets the user's password by hashing the provided password.

        Args:
            password (str): Password to be hashed and set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the user's hashed password.

        Args:
            password (str): Password to be checked.

        Returns:
            bool: True if the password matches the user's hashed password, False otherwise.
        """
        return check_password_hash(self.password_hash, password)


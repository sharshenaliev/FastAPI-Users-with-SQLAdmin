from dotenv import load_dotenv
import os
from passlib.context import CryptContext


context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

load_dotenv()

ADMIN_USERNAME = os.environ.get("LOGIN")
ADMIN_PASSWORD = os.environ.get("PASSWORD")

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    MONGODB_URL = os.getenv("MONGODB_URL") or "mongodb://localhost:27017"
    DATABASE_NAME = os.getenv("DATABASE_NAME") or "hospital_db"

    JWT_SECRET = os.getenv("JWT_SECRET") or "your_secret"
    ALGORITHM = os.getenv("ALGORITHM") or "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60
    )

    BASE_URL = os.getenv("BASE_URL") or "http://localhost:8000"

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT") or 587)

    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


    # -----------------------------
    # GOOGLE OAUTH
    # -----------------------------
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


settings = Settings()
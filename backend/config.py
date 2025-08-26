import os

class Settings:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "rhorizon")
    DB_USER = os.getenv("DB_USER", "rhorizon")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "rhorizon")
    DB_SSLMODE = os.getenv("DB_SSLMODE", "prefer")  # 'require' for RDS prod

    AWS_REGION = os.getenv("AWS_REGION", "eu-west-3")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")  # required in prod

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?sslmode={self.DB_SSLMODE}"
        )

settings = Settings()

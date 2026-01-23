import os

os.environ["APP_ENV"] = "production"
print(os.getenv("APP_ENV"))

from os import getenv

EMAIL_FROM = getenv('EMAIL_FROM', 'noreply@edm.su')

SECRET_KEY = getenv('SECRET_KEY', 'bhdasbdashjcxjhzbjhdasjhdasdbasj')

STATIC_URL = getenv('STATIC_URL', 'https://static.dev.edm.su')

DB_DRIVER = getenv('DB_DRIVER', 'postgresql')
DB_USERNAME = getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = getenv('DB_PASSWORD', ' ')
DB_HOST = getenv('DB_HOST', 'old_db')
DB_PORT = getenv('DB_PORT', 5432)
DB_NAME = getenv('DB_NAME', 'postgres')
DATABASE_URL = getenv('DATABASE_URL', 'postgresql://postgres:postgres@old_db/postgres')

FRONTEND_URL = getenv('FRONTEND_URL', 'https://edm.su')

SENDGRID_API_KEY = getenv('SENDGRID_API_KEY')

YOUTUBE_API_KEY = getenv('YOUTUBE_API_KEY')

ALGOLIA_APP_ID = getenv('ALGOLIA_APP_ID')
ALGOLIA_API_KEY = getenv('ALGOLIA_API_KEY')
ALGOLIA_INDEX = getenv('ALGOLIA_INDEX')

S3_BUCKET = getenv('S3_BUCKET')
S3_ENDPOINT = getenv('S3_ENDPOINT')
S3_ACCESS_KEY = getenv('S3_ACCESS_KEY')
S3_ACCESS_KEY_ID = getenv('S3_ACCESS_KEY_ID')

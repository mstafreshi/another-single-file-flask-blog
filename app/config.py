import os

class Config:
    PROJECT_NAME = os.environ.get("PROJECT_NAME") or "Flask CMS"
    SECRET_KEY = 'HARD-To-GUESS-VALUE'
    LANG_CODES = ['en', 'es', 'fa']
    DEFAULT_LANG_CODE = os.environ.get('DEFAULT_LANG_CODE') or 'en'
    ADMINISTRATOR_EMAIL= os.environ.get('ADMINISTRATOR_EMAIL') or 'your-email@example.com'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') \
        or 'mysql://username:password@host/database'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = os.environ.get('SQLALCHEMY_COMMIT_ON_TEARDOWN') or False
    
config = {
    'default': Config
}

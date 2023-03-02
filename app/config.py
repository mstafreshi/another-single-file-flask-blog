import os

class Config:
    SECRET_KEY = 'KhodayeMan'
    PROJECT_NAME = os.environ.get("PROJECT_NAME") or "Flask Blog"
    ##SQLALCHEMY_DATABASE_URI = 'mysql://root:mohsen@localhost/mstafreshi'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE") or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    
config = {
    'default': Config
}

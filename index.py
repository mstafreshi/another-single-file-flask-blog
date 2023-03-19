from app import create_app, db, cli
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)
cli.register(app)

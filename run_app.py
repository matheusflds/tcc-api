from flask_migrate import Migrate

from app.routes import setup_routes
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)
setup_routes(app)

if __name__ == "__main__":
  app.run(debug=True)

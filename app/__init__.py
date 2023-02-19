from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from pathlib import Path
# define the app
app = Flask(__name__)


# added for hashing the passwords
bcrypt = Bcrypt(app)

# added to fix RuntimeError: Working outside of application context.
app.app_context().push()

# read configuration from config.py file
app.config.from_object('config')

# check if there is a file called "app.py" in the outside folder
# if so we are in the EC2 instance and we DO NOT want to include the CORS(app) line below
path = Path("app.py")
if not Path.is_file(path):
    # added to enable cors
    CORS(app)
    print("CORS included, we're on local because there's no app.py")
else:
    print("app.py detected, we're on EC2, don't include CORS in __init__.py")

# define the database
db = SQLAlchemy(app)

# helps us handle migrations
migrate = Migrate(app, db)

# import these python files from /app directory
from app import views, models  # noqa: E402, F401

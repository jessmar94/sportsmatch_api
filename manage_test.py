import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from createdb import createdb
from dotenv import load_dotenv
load_dotenv()

from src.app import create_app, db

createdb(os.getenv('TEST_DATABASE_URL'))

env_name = os.getenv('FLASK_ENV_TEST')
app = create_app(env_name)

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()

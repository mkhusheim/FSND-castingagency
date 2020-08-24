from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import APP
from . import models

db.init_app(APP)
migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

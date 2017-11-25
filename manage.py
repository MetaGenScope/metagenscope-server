"""Command line tools for Flask server app."""

import unittest
import coverage

from flask_script import Manager
from flask_migrate import MigrateCommand

from app import create_app, db
from app.api.models import User, Organization


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*'
    ]
)
COV.start()


app = create_app()
manager = Manager(app)  # pylint: disable=invalid-name
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the tests without code coverage."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Run the unit tests with coverage."""
    tests = unittest.TestLoader().discover('app/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreate a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seed the database."""
    db.session.add(User(username='bchrobot', email="benjamin.blair.chrobot@gmail.com", password='Foobar22'))
    db.session.add(User(username='benjaminchrobot', email="benjamin.chrobot@alum.mit.edu", password='Foobar22'))
    db.session.add(Organization(name='Mason Lab', adminEmail='benjamin.blair.chrobot@gmail.com'))
    db.session.commit()


if __name__ == '__main__':
    manager.run()

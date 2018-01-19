"""Command line tools for Flask server app."""

import unittest
import coverage

from flask_script import Manager
from flask_migrate import MigrateCommand, upgrade

from app import create_app, db
from app.users.user_models import User
from app.organizations.organization_models import Organization
from app.query_results.query_result_models import QueryResult
from app.sample_groups.sample_group_models import SampleGroup

from seed.sample_similarity import sample_similarity


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'tests/*'
    ]
)
COV.start()


app = create_app()
manager = Manager(app)  # pylint: disable=invalid-name
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the tests without code coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Run the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
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
    """Recreate a database using migrations."""
    # We cannot simply use db.drop_all() because it will not drop the alembic_versions table
    sql = "SELECT \
        'drop table if exists \"' || tablename || '\" cascade;' as pg_drop \
        FROM \
        pg_tables \
        WHERE \
        schemaname='public';"

    drop_statements = db.engine.execute(sql)
    if drop_statements.rowcount > 0:
        drop_statement = "\n".join([x['pg_drop'] for x in drop_statements])
        drop_statements.close()
        db.engine.execute(drop_statement)

    # Run migrations
    upgrade()


@manager.command
def seed_db():
    """Seed the database."""
    bchrobot = User(username='bchrobot',
                    email="benjamin.blair.chrobot@gmail.com",
                    password='Foobar22')
    dcdanko = User(username='dcdanko',
                   email="dcd3001@med.cornell.edu",
                   password='Foobar22')
    cmason = User(username='cmason',
                  email="chm2042@med.cornell.edu",
                  password='Foobar22')
    db.session.add(bchrobot)
    db.session.add(dcdanko)
    db.session.add(cmason)

    mason_lab = Organization(name='Mason Lab', admin_email='benjamin.blair.chrobot@gmail.com')
    db.session.add(mason_lab)
    mason_lab.users = [bchrobot, dcdanko, cmason]

    sample_group = SampleGroup(name='MetaSub Pilot 2017')
    db.session.add(sample_group)

    db.session.commit()

    QueryResult(sample_similarity=sample_similarity, sample_group_id=sample_group.id).save()


if __name__ == '__main__':
    manager.run()

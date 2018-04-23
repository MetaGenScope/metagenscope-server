"""Command line tools for Flask server app."""

import unittest
import coverage


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'tests/*',
        '*/test_*.py',
        '*/tests/*',
    ]
)
COV.start()


from flask_script import Manager
from flask_migrate import MigrateCommand, upgrade

from app import create_app, db
from app.users.user_models import User
from app.organizations.organization_models import Organization
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup

from seed import abrf_analysis_result, uw_analysis_result, reads_classified


app = create_app()
manager = Manager(app)  # pylint: disable=invalid-name
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the tests without code coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    tests.addTests(unittest.TestLoader().discover('./app', pattern='test*.py'))
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Run the unit tests with coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    tests.addTests(unittest.TestLoader().discover('./app', pattern='test*.py'))
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
    sql = 'SELECT \
        \'drop table if exists "\' || tablename || \'" cascade;\' as pg_drop \
        FROM \
        pg_tables \
        WHERE \
        schemaname=\'public\';'

    drop_statements = db.engine.execute(sql)
    if drop_statements.rowcount > 0:
        drop_statement = '\n'.join([x['pg_drop'] for x in drop_statements])
        drop_statements.close()
        db.engine.execute(drop_statement)

    # Run migrations
    upgrade()

    # Empty Mongo database
    AnalysisResultMeta.drop_collection()
    Sample.drop_collection()


@manager.command
def seed_db():
    """Seed the database."""
    bchrobot = User(username='bchrobot',
                    email='benjamin.blair.chrobot@gmail.com',
                    password='Foobar22')
    dcdanko = User(username='dcdanko',
                   email='dcd3001@med.cornell.edu',
                   password='Foobar22')
    cmason = User(username='cmason',
                  email='chm2042@med.cornell.edu',
                  password='Foobar22')


    abrf_analysis_result_01 = AnalysisResultMeta(reads_classified=reads_classified).save()
    abrf_sample_01 = Sample(name='SomethingUnique_A', theme='world-quant-sample',
                            analysis_result=abrf_analysis_result_01).save()
    abrf_analysis_result_02 = AnalysisResultMeta(reads_classified=reads_classified).save()
    abrf_sample_02 = Sample(name='SomethingUnique_B', theme='world-quant-sample',
                            analysis_result=abrf_analysis_result_02).save()
    abrf_analysis_result.save()
    abrf_description = 'ABRF San Diego Mar 24th-29th 2017'
    abrf_2017_group = SampleGroup(name='ABRF 2017', analysis_result=abrf_analysis_result,
                                  description=abrf_description, theme='world-quant')
    abrf_2017_group.samples = [abrf_sample_01, abrf_sample_02]

    uw_analysis_result.save()
    uw_sample = Sample(name='UW_Madison_00', analysis_result=uw_analysis_result).save()
    uw_group_result = AnalysisResultMeta().save()
    uw_madison_group = SampleGroup(name='The UW Madison Project',
                                   analysis_result=uw_group_result)
    uw_madison_group.samples = [uw_sample]

    mason_lab = Organization(name='Mason Lab', admin_email='benjamin.blair.chrobot@gmail.com')
    mason_lab.users = [bchrobot, dcdanko, cmason]
    mason_lab.sample_groups = [abrf_2017_group, uw_madison_group]

    db.session.add(mason_lab)
    db.session.commit()

    mason_lab.add_admin(bchrobot)
    mason_lab.add_admin(dcdanko)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

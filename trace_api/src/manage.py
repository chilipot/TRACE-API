#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

from flask import session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model.tables import Term

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(host="0.0.0.0", port=5000)


@manager.command
def test():
    """
    Runs the unit tests.
    """
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


# This is necessary to stay here until flask restplus allows for this to be moved inside a sub namespace
@app.before_first_request
def load_cached_terms():
    session.clear()
    if session.get('cached_terms', None) is None:
        session['cached_terms'] = [x.Title.split(":")[-1].strip().replace(' - ', ' ')
                                   for x in Term.query.with_entities(Term.Title).all()]


if __name__ == '__main__':
    manager.run()

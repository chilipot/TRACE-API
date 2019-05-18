import os
from api import create_app, db_session
from flask_script import Manager
from api.controller import api

app = create_app(os.getenv('APP_ENV') or 'dev')

# Loads all routes into Blueprint
from api.controller import instructor_controller, report_controller, term_controller, department_controller, survey_controller
app.register_blueprint(api)


@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()


app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run(debug=app.config.get('DEBUG'))


if __name__ == '__main__':
    manager.run()

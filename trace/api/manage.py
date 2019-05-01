import os
from api import create_app
from flask_script import Manager
from api.controller import api

app = create_app(os.getenv('APP_ENV') or 'dev')

# Loads all routes into Blueprint
from api.controller import instructor_controller, report_controller, term_controller, department_controller
app.register_blueprint(api)

app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run(debug=app.config.get('DEBUG'))


if __name__ == '__main__':
    manager.run()

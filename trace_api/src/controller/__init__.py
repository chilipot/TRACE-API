from flask import Blueprint
from flask_restplus import Api
from src.controller.auth_controller import api as auth_ns
from src.controller.report_controller import api as report_ns
from src.controller.user_controller import api as user_ns



blueprint = Blueprint('api',
                      __name__,
                      url_prefix="/api/v1")

api = Api(app=blueprint,
          title='TRACE API',
          version='1.0',
          description='Northeastern\'s Course Evaluation API')
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(report_ns, path='/report')

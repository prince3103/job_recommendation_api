from flask_restful import Resource
from flask_jwt import jwt_required

class LoggedUserData(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'You Are Logged In'}
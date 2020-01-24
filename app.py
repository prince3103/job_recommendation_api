import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

# from security import authenticate, identity
from security import authenticate, identity as identity_function
from resources.user import UserRegister, UserCVUpload

UPLOAD_FOLDER = "CV"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email_address'
# jwt = JWT(app, authenticate, identity)  # /auth

jwt = JWT(app, authenticate, identity_function)

@jwt.auth_response_handler
def customized_response_handler(access_token, user):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'name': user.name,
                        'email_address': user.email_address
                   })

api.add_resource(UserRegister, '/register')
api.add_resource(UserCVUpload, '/user_cv_upload')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    
    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)

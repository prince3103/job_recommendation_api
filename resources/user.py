from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email_address',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if data['email_address']=="":
            return {"message": "Email Address cannot be blank"}, 400
        if data['password']=="":
            return {"message": "Password cannot be blank"}, 400    

        if UserModel.find_by_email_address(data['email_address']):
            return {"message": "A user with that email_address already exists"}, 400

        user = UserModel(data['email_address'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

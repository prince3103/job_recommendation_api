from flask_restful import Resource, reqparse
from flask import request
from models.user import UserModel
from flask_jwt import jwt_required

import os
from flask import Flask, request
from werkzeug.utils import secure_filename


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
    parser.add_argument('name',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('phone_number',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('zip_code',
                        type=str,
                        required=False,
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

        user = UserModel(data['email_address'], data['password'] , data['name'] , data['phone_number'] , data['zip_code'], "")
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserCVUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email_address',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def put(self):
        if 'file' not in request.files:
            return {'message' : 'No file part in the request'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'message' : 'No file selected for uploading'}, 400
        if file and UserModel.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("CV", filename))


            data = UserCVUpload.parser.parse_args()
            print(data['email_address'])

            if data['email_address']=="":
                return {"message": "Email Address cannot be blank"}, 400
            user = UserModel.find_by_email_address(data['email_address'])
            print(user.email_address)
            user.cv_path="CV/"+str(filename)
            user.save_to_db()
            return {'message' : 'File successfully uploaded'}, 201
                
        return {'message' : 'Allowed file types are pdf, doc'}, 400
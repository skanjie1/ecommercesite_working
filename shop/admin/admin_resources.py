from flask_restful import Resource, reqparse
from .models import User
from shop import app, db, bcrypt
from flask_jwt_extended import create_access_token
from flask_bcrypt import check_password_hash

class AdminRegistrationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        hash_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')
        user = User(name=args['name'], username=args['username'], email=args['email'], password=hash_password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'Registration successful'}, 201

class AdminLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()
        if user and check_password_hash(user.password, args['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

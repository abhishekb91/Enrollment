from flask import jsonify
from flask_restplus import Resource

from application import api
from application.models import User


@api.route('/api/users', '/api/users/')
class GetAndPostUser(Resource):

    def get(self):
        return jsonify(User.objects().all())

    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'],
                    last_name=data['last_name'])
        user.set_password(password=data['password'])
        user.save()

        return jsonify(User.objects(user_id=data['user_id']).first())


@api.route('/api/users/<idx>', '/api/users/<idx>/')
class GetUpdateAndDeleteUser(Resource):

    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx).first())

    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify('User successfully deleted!')

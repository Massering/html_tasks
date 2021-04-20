from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data.db_session import create_session
from data.users import User


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = create_session()
        users = session.query(User).get(user_id)
        return jsonify({'users': users.to_dict(
            only=('surname', 'name', 'position', 'address', 'age', 'speciality', 'email'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'position', 'address', 'age', 'speciality', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        user = User(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_users_not_found(id):
    if not create_session().query(User).get(id):
        abort(404, message=f"User #{id} not found")


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)

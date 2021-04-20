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

        if args['password'] != args['password_again']:
            abort(400, message='Passwords are not the same')

        if session.query(User).filter(User.email == args['email']).first():
            abort(400, message='User with that email already exist')

        user = User(
            email=args['email'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_users_not_found(id):
    if not create_session().query(User).get(id):
        abort(404, message=f"User #{id} not found")


parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('password_again', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', type=int)
parser.add_argument('position')
parser.add_argument('speciality')
parser.add_argument('address')

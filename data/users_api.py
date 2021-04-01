from flask import jsonify, Blueprint, request, render_template

from . import db_session
from .users import User
from data.yandex_maps import save_picture_by_name

from werkzeug.security import generate_password_hash

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict()
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_user_by_id(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    return jsonify(user.to_dict())


@blueprint.route('/users_show/<int:user_id>')
def get_city_by_id(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(user_id)).first()

    picture_filename = f'/static/img/cities/city_of_user_{user_id}.png'
    save_picture_by_name(user.city_from, picture_filename[1:])

    return render_template('user_city_view.html',
                           title=f'Родной город астронавта {user.surname} {user.name}',
                           img_filename=picture_filename,
                           city_name=user.city_from
                           )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    required_keys = ['surname', 'name', 'age', 'position',
                     'speciality', 'address', 'email', 'hashed_password']
    if not all(key in request.json for key in required_keys):
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    if 'id' in request.json and session.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})

    if request.json.get('password', None):
        request.json['hashed_password'] = generate_password_hash(request.json['password'])

    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
    )
    session.add(user)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if 'id' not in request.json:
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'User not exists'})

    session.delete(user)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if 'id' not in request.json:
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'user not exists'})

    for key, value in request.json.items():
        if key == 'surname':
            user.surname = value
        elif key == 'name':
            user.name = value
        elif key == 'age':
            user.age = value
        elif key == 'position':
            user.position = value
        elif key == 'speciality':
            user.speciality = value
        elif key == 'address':
            user.address = value
        elif key == 'email':
            user.email = value
        elif key == 'hashed_password':
            user.hashed_password = value
        elif key == 'password':
            user.set_password(value)

    session.commit()

    return jsonify({'success': 'OK'})

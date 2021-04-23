from flask_restful import reqparse


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

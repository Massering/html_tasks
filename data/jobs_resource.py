from flask_restful import abort, Resource
from flask import jsonify

from data.db_session import create_session
from data.users import User
from data.jobs import Jobs
from data.categories import Category
from data.job_parser import parser


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = create_session()
        jobs = session.query(Jobs).get(job_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'category', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'category', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = create_session()

        collaborators = []
        for collaborator_fio in args['collaborators'].split(', '):
            surname, name = collaborator_fio.split()
            collaborator = session.query(User).filter(User.name == name, User.surname == surname).first()
            if not collaborator:
                abort(404, message=f'User "{collaborator_fio}" is not found')
            collaborators.append(str(collaborator.id))

        surname, name = args['team_leader'].split()
        team_leader = session.query(User).filter(User.name == name, User.surname == surname).first()
        if not team_leader:
            abort(404, message=f'User "{args["team_leader"]}" is not found')

        category = session.query(Category).filter(Category.name == args['category']).first()
        if not category:
            abort(404, message=f'Category "{args["category"]}" is not found')

        job = Jobs(
            team_leader=team_leader.id,
            job=args['job'],
            work_size=args['work_size'],
            collaborators=', '.join(collaborators),
            category=category.id,
            start_date=args.get('start_date', None),
            end_date=args.get('end_date', None),
            is_finished=args.get('is_finished', None),
        )

        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_job_not_found(id):
    if not create_session().query(Jobs).get(id):
        abort(404, message=f"Job #{id} is not found")

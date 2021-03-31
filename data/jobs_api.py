from flask import jsonify, Blueprint, request

from . import db_session
from .jobs import Jobs

blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_job():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_job_by_id(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    return jsonify(job.to_dict())


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in
               ['team_leader', 'job', 'work_size', 'collaborators']):
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    if 'id' in request.json and session.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})

    job = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators']
    )
    session.add(job)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if 'id' not in request.json:
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'Job not exists'})

    session.delete(job)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if 'id' not in request.json:
        return jsonify({'error': 'Bad request'})

    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'Job not exists'})

    for key, value in request.json.items():
        if key == 'team_leader':
            job.team_leader = value
        elif key == 'job':
            job.job = value
        elif key == 'work_size':
            job.work_size = value
        elif key == 'collaborators':
            job.collaborators = value
        elif key == 'start_date':
            job.start_date = value
        elif key == 'end_date':
            job.end_date = value
        elif key == 'is_finished':
            job.is_finished = value

    session.commit()

    return jsonify({'success': 'OK'})

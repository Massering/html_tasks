from flask import Flask, render_template, url_for, request, make_response, redirect
import requests

from data.db_session import global_init, create_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/jobs')
def job_list():
    session = create_session()

    titles = ['Title', 'Team leader', 'Duration', 'Collaborators', 'Is finished']
    jobs = [job.values(session) for job in session.query(Jobs).all()]
    sizes = [220, 120, 100, 50, 100]

    return render_template('list_view.html', table_title='Jobs list',
                           title='Список работ', column_sizes=sizes, titles=titles, list=jobs)


if __name__ == '__main__':
    global_init('db/blogs.db')

    app.run(debug=True)

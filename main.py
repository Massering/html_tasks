from flask import Flask, render_template, request, make_response, redirect, jsonify

from data import jobs_api
from data.db_session import global_init, create_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department

from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def homepage():
    links = [
        ('/jobs', 'Лист работ'),
        ('/register', 'Регистрация'),
        ('', ''),
    ]
    return render_template('home_page.html', title='Домашняя страница', links=links)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/jobs')
def job_list():    # http://127.0.0.1:5000/jobs
    session = create_session()

    titles = ['Title', 'Team leader', 'Duration', 'Collaborators', 'Is finished']
    jobs = [job.values(session) for job in session.query(Jobs).all()]
    sizes = [220, 120, 100, 50, 100]

    return render_template('list_view.html', table_title='Jobs list',
                           title='Список работ', column_sizes=sizes, titles=titles, list=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():    # http://127.0.0.1:5000/register
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_form.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register_form.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже существует")

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/successful_register')
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/successful_register')
def successful_registr():
    return render_template('successful_register_form.html', title='Успешно!')


if __name__ == '__main__':
    global_init('db/blogs.db')

    app.register_blueprint(jobs_api.blueprint)
    app.run(debug=True)

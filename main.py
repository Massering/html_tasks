from flask import Flask, render_template, make_response, redirect, jsonify

from data import jobs_api
from data import users_api
from data.db_session import global_init, create_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department

from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm
from forms.departments import DepartmentsForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
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
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def jobs_list():
    session = create_session()

    titles = ['Title', 'Team leader', 'Duration', 'Collaborators', 'Is finished']
    jobs = [job.values() for job in session.query(Jobs).all()]
    sizes = [220, 120, 100, 180, 100]

    return render_template('jobs.html', title='Список работ',
                           column_sizes=sizes, titles=titles, list=jobs, current_user=current_user)


@app.route('/add_job',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()

    if form.validate_on_submit():
        session = create_session()
        job = Jobs()

        job.team_leader = session.query(User).filter(User.email == current_user.email).first().id
        job.job = form.job.data
        job.work_size = form.work_size.data
        collaborators = []
        for collaborator in form.collaborators.data.split(','):
            surname, name = collaborator.split()
            collaborators.append(session.query(User).filter(User.surname == surname, User.name == name).first().id)
        job.collaborators = ', '.join(map(str, collaborators))
        job.is_finished = form.is_finished.data

        session.add(job)
        session.commit()

        return redirect('/')

    return render_template('job.html', title=f"Добавление работы", form=form)


@app.route('/add_job/<int:id>',  methods=['GET', 'POST'])
@login_required
def update_job(id):
    form = JobsForm()

    if form.validate_on_submit():
        session = create_session()
        job = session.query(Jobs).filter(Jobs.id == id).first()

        job.job = form.job.data
        job.work_size = form.work_size.data
        collaborators = []
        for collaborator in form.collaborators.data.split(','):
            surname, name = collaborator.split()
            collaborators.append(session.query(User).filter(User.surname == surname,
                                                            User.name == name).first().id)
        job.collaborators = ', '.join(map(str, collaborators))
        job.is_finished = form.is_finished.data

        session.commit()

        return redirect('/')

    session = create_session()
    job = session.query(Jobs).filter(Jobs.id == id).first()
    if current_user.id != 1 and current_user.id != job.team_leader:
        return redirect('/')
    form.job.data = job.job
    form.work_size.data = job.work_size
    collaborators = []
    for collaborator in job.collaborators.split(', '):
        collaborators.append(session.query(User).filter(User.id == collaborator).first().fio())
    form.collaborators.data = ', '.join(collaborators)
    form.is_finished.data = job.is_finished

    return render_template('job.html', title=f"Редактирование работы", form=form)


@app.route('/delete_job/<int:id>',  methods=['GET', 'DELETE'])
@login_required
def delete_job(id):
    session = create_session()
    job = session.query(Jobs).filter(Jobs.id == id).first()

    if current_user.id == 1 or current_user.id == job.team_leader:
        session.delete(job)
        session.commit()

    return redirect('/')


@app.route('/departments')
def departments_list():
    session = create_session()

    titles = ['Title', 'Chief', 'Email', 'Members']
    departments = [department.values() for department in session.query(Department).all()]
    sizes = [220, 140, 150, 220]

    return render_template('departments.html', title='Список департаментов',
                           column_sizes=sizes, titles=titles, list=departments, current_user=current_user)


@app.route('/add_department',  methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentsForm()

    if form.validate_on_submit():
        session = create_session()
        department = Department()

        department.chief = session.query(User).filter(User.email == current_user.email).first().id
        department.title = form.title.data
        department.email = form.email.data
        members = []
        for member in form.members.data.split(','):
            surname, name = member.split()
            members.append(session.query(User).filter(User.surname == surname, User.name == name).first().id)
        department.members = ', '.join(map(str, members))

        session.add(department)
        session.commit()

        return redirect('/departments')

    return render_template('department.html', title=f"Добавление департамента", form=form)


@app.route('/add_department/<int:id>',  methods=['GET', 'POST'])
@login_required
def update_department(id):
    form = DepartmentsForm()

    if form.validate_on_submit():
        session = create_session()
        department = session.query(Department).filter(Department.id == id).first()

        department.title = form.title.data
        department.email = form.email.data
        members = []
        for member in form.members.data.split(','):
            surname, name = member.split()
            members.append(session.query(User).filter(User.surname == surname,
                                                            User.name == name).first().id)
        department.members = ', '.join(map(str, members))

        session.commit()

        return redirect('/departments')

    session = create_session()
    department = session.query(Department).filter(Department.id == id).first()
    if current_user.id != 1 and current_user.id != department.chief:
        return redirect('/departments')
    form.title.data = department.title
    form.email.data = department.email
    members = []
    for member in department.members.split(', '):
        members.append(session.query(User).filter(User.id == member).first().fio())
    form.members.data = ', '.join(members)

    return render_template('department.html', title="Редактирование департамента", form=form)


@app.route('/delete_department/<int:id>',  methods=['GET', 'DELETE'])
@login_required
def delete_department(id):
    session = create_session()
    department = session.query(Department).filter(Department.id == id).first()

    if current_user.id == 1 or current_user.id == department.chief:
        session.delete(department)
        session.commit()

    return redirect('/departments')


if __name__ == '__main__':
    global_init('db/blogs.db')

    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(debug=True)

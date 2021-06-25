from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user

from app import db
from models import Attempt, Group, Task, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

#@main.route('/profile')
#@login_required
#def profile():
#    return render_template('profile.html', name=current_user.name)

@main.route('/user/<int:id>/attempts')
@login_required
def attempts(id):
    if( not current_user.is_instructor() and id != current_user.id):
        abort(401)
    attempts = Attempt.query.filter_by(user_id=id).order_by(Attempt.date.desc()).all()
    for attempt in attempts:
        total_tasks = 0
        right_tasks = 0
        for task in attempt.tasks:
            total_tasks += 1
            if task.result:
                right_tasks += 1

        attempt.total_tasks = total_tasks
        attempt.right_tasks = right_tasks
        attempt.is_success = True if total_tasks - right_tasks < right_tasks else False 

    return render_template('attempts.html', attempts=attempts)


@main.route('/set_result',  methods=['POST'])
def result():
    try:
        user_id = request.form['id']
        elapsed_time = request.form['elapsed_time']
        total_time = request.form['total_time']
        task_count = request.form['task_count']
        solved_tasks = [int(x) for x in request.form['solved_tasks'].split(',')]
        task_types = [int(x) for x in request.form['task_types'].split(',')]
    except:
        return 'fail'

    try:
        new_attempt = Attempt(elapsed_time=int(elapsed_time),
        total_time=int(total_time), user_id=int(user_id))

        db.session.add(new_attempt)
        db.session.flush()

        for i in range(int(task_count)):
            type = task_types[i]
            result=True if i + 1 in solved_tasks else False

            new_task = Task(attempt_id=new_attempt.id, type=type,
             result=result, number=i + 1)
            db.session.add(new_task)

        db.session.commit()
        return 'success'

    except:
        db.session.rollback()
        print('Database add exception')
        return 'fail'


@main.route('/groups')
@login_required
def groups():
    if( not current_user.is_instructor()):
        abort(401)
    groups = Group.query.order_by(Group.year.desc(), Group.name, Group.number).all()
    return render_template('groups.html', groups=groups)

@main.route('/groups/<int:id>')
@login_required
def groups_users(id):
    if( not current_user.is_instructor()):
        abort(401)
    groups = Group.query.order_by(Group.year.desc(), Group.name, Group.number).all()
    group = Group.query.filter_by(id=id).first()

    return render_template('groups.html', groups=groups,
     current_group=f'{group.name}-{group.number}-{group.year}', users=group.users)
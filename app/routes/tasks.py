from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task
from app.models import User

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/viewtasks')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    current_user = User.query.filter_by(username=session['user']).first()

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods = ["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    time = request.form.get('time')
    date = request.form.get('date')
    day = request.form.get('day')
    if title:
        current_user = User.query.filter_by(username=session['user']).first()

    # Find the next task_number for this user
        last_task = Task.query.filter_by(user_id=current_user.id).order_by(Task.task_number.desc()).first()
        next_number = (last_task.task_number + 1) if last_task else 1

        new_task = Task(title=title, time=time, date=date, day=day, user_id=current_user.id, task_number=next_number)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('tasks.view_tasks'))

    return redirect(url_for('tasks.add_task')) 

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'

        db.session.commit()
    
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods = ["POST"])
def clear_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    current_user = User.query.filter_by(username=session['user']).first()
    # Delete only this user's tasks
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_tasks'))



@tasks_bp.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    task = Task.query.get(task_id)
    user_id = task.user_id
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'warning')

        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.task_number).all()
        for i, t in enumerate(tasks, start=1):
            t.task_number = i
        db.session.commit()
    
    return redirect(url_for('tasks.view_tasks'))


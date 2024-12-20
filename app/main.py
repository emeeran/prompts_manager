from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Prompt
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    prompts = Prompt.query.filter_by(user_id=current_user.id)\
        .order_by(Prompt.created_at.desc())\
        .all()
    return render_template('home.html', prompts=prompts)

@main.route('/add', methods=['POST'])
@login_required
def add_prompt():
    title = request.form['title']
    content = request.form['content']
    prompt = Prompt(title=title, content=content, user_id=current_user.id)
    db.session.add(prompt)
    db.session.commit()
    flash("Prompt added!", "success")
    return redirect(url_for('main.home'))

@main.route('/delete/<int:id>')
@login_required
def delete_prompt(id):
    prompt = Prompt.query.get(id)
    if prompt and prompt.user_id == current_user.id:
        db.session.delete(prompt)
        db.session.commit()
        flash("Prompt deleted!", "success")
    else:
        flash("Unauthorized action.", "danger")
    return redirect(url_for('main.home'))

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_prompt(id):
    prompt = Prompt.query.get_or_404(id)
    if prompt.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        prompt.title = request.form['title']
        prompt.content = request.form['content']
        db.session.commit()
        flash('Prompt updated!', 'success')
        return redirect(url_for('main.home'))

    return render_template('edit_prompt.html', prompt=prompt)

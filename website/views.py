from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data.decode('utf-8'))
    note_id = data['noteID']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/edit-note/<int:id_>', methods=['GET', 'POST'])
@login_required
def edit_note(id_):
    note = Note.query.get(id_)
    if request.method == 'POST':
        note.data = request.form.get('note')
        db.session.commit()
        return redirect(url_for('views.home'))

    return render_template('update.html', note=note, user=current_user)

from flask import Blueprint, render_template, url_for, request, jsonify, flash
from flask_login import login_required, current_user
from . import db
from .models import Announcement
from .models import UserFavorite
import json

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    announcements = Announcement.query.all()
    return render_template('home.html', announcements=announcements, user=current_user)

@views.route('/save-favorite', methods=['GET', 'POST'])
@login_required
def save_favorite():
    data = request.get_json()
    announcement_id = data.get('id')

    if not announcement_id:
        return jsonify({"error": "ID-ul anunțului lipsește"}), 400

    existing_favorite = UserFavorite.query.filter_by(user_id=current_user.id, announcement_id=announcement_id).first()
    if existing_favorite:
        flash('Acest anunt este deja salvat!', category='error')
        return jsonify({"error":"Anuntul este deja salvat"}), 400

    favorite = UserFavorite(user_id=current_user.id, announcement_id=announcement_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"error":"Anunt salvat cu succes"})

@views.route('/favorites')
@login_required
def favorites():

    return render_template('favorites.html', user=current_user)

@views.route('/delete-favorite', methods=['POST'])
@login_required
def delete_favorite():
    data = json.loads(request.data)
    fav_id = data.get('favId')
    fav = UserFavorite.query.get(fav_id)

    if fav:
        if fav.user_id == current_user.id:
            db.session.delete(fav)
            db.session.commit()

    return jsonify({})
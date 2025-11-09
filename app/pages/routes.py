from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils import validate_id, validate_ownership
from app.models import Collection, Resource

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/login')
def login_page():
    return render_template('login.html')


@pages_bp.route('/')
def index_redirect():
    from flask_login import current_user
    # If user is already logged in, redirect to collections
    if current_user.is_authenticated:
        return redirect(url_for('pages.collections_page'))
    # Otherwise show login page
    return render_template('login.html')


@pages_bp.route('/register')
def register_page():
    return render_template('register.html')


@pages_bp.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')


@pages_bp.route('/profile/edit')
@login_required
def edit_profile_page():
    return render_template('edit_profile.html')


@pages_bp.route('/faq')
@login_required
def faq_page():
    return render_template('faq.html')


@pages_bp.route('/help')
def public_faq_page():
    return render_template('public_faq.html')


@pages_bp.route('/collections')
@login_required
def collections_page():
    return render_template('collections.html')


@pages_bp.route('/collections/new')
@login_required
def new_collection_page():
    return render_template('new_collection.html')


@pages_bp.route('/collections/<int:cid>')
@login_required
def collection_detail_page(cid):
    try:
        cid = validate_id(cid, "Collection ID")
        collection = validate_ownership(Collection, cid)
        return render_template('collection_detail.html')
    except Exception as e:
        flash('Collection not found or access denied.', 'error')
        return redirect(url_for('pages.collections_page'))


@pages_bp.route('/collections/<int:cid>/resources/new')
@login_required
def new_resource_page(cid):
    try:
        cid = validate_id(cid, "Collection ID")
        collection = validate_ownership(Collection, cid)
        return render_template('new_resource.html')
    except Exception as e:
        flash('Collection not found or access denied.', 'error')
        return redirect(url_for('pages.collections_page'))


@pages_bp.route('/profile/change-password')
@login_required
def change_password_page():
    return render_template('change_password.html')


@pages_bp.route('/collections/<int:cid>/edit')
@login_required
def edit_collection_page(cid):
    try:
        cid = validate_id(cid, "Collection ID")
        collection = validate_ownership(Collection, cid)
        return render_template('edit_collection.html')
    except Exception as e:
        flash('Collection not found or access denied.', 'error')
        return redirect(url_for('pages.collections_page'))


@pages_bp.route('/resources/<int:rid>/edit')
@login_required
def edit_resource_page(rid):
    try:
        rid = validate_id(rid, "Resource ID")
        resource = validate_ownership(Resource, rid)
        return render_template('edit_resource.html')
    except Exception as e:
        flash('Resource not found or access denied.', 'error')
        return redirect(url_for('pages.collections_page'))

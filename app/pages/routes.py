from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/login')
def login_page():
    return render_template('login.html')


@pages_bp.route('/')
def index_redirect():
    # simple root redirect to login
    return render_template('login.html')


@pages_bp.route('/register')
def register_page():
    return render_template('register.html')


@pages_bp.route('/profile')
def profile_page():
    return render_template('profile.html')


@pages_bp.route('/profile/edit')
def edit_profile_page():
    return render_template('edit_profile.html')


@pages_bp.route('/faq')
def faq_page():
    return render_template('faq.html')


@pages_bp.route('/collections')
def collections_page():
    return render_template('collections.html')


@pages_bp.route('/collections/new')
def new_collection_page():
    return render_template('new_collection.html')


@pages_bp.route('/collections/<int:cid>')
def collection_detail_page(cid):
    return render_template('collection_detail.html')


@pages_bp.route('/collections/<int:cid>/resources/new')
def new_resource_page(cid):
    return render_template('new_resource.html')


@pages_bp.route('/profile/change-password')
def change_password_page():
    return render_template('change_password.html')


@pages_bp.route('/collections/<int:cid>/edit')
def edit_collection_page(cid):
    return render_template('edit_collection.html')


@pages_bp.route('/resources/<int:rid>/edit')
def edit_resource_page(rid):
    return render_template('edit_resource.html')

from flask import Blueprint, render_template
from flask_login import login_required


views = Blueprint('views', __name__, url_prefix='/')

@views.route('/')
@views.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@views.route('/posts')
@login_required
def posts_page():
    return render_template('post.html')
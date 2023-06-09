from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import PostForm, DeleteForm, UpdateForm
from .models import Post
from . import db
from datetime import datetime


views = Blueprint('views', __name__, url_prefix='/')

@views.route('/')
@views.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@views.route('/posts')
@login_required
def posts_page():
     form = DeleteForm()
     update_form = UpdateForm()
     posts = Post.query.order_by(Post.id).all()
     for post in posts:
         post.created_at = datetime.strptime(str(post.created_at), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S")
     
     return render_template('post.html', posts=posts, form=form, update_form = update_form)
    

@views.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post_page():
    form = PostForm()
    if form.validate_on_submit():
       new_post = Post(
           title=form.title.data, 
           content=form.content.data,
           owner_id=current_user.id
           )
       db.session.add(new_post)
       db.session.commit()
       flash('Post Created!', category='success')
       return redirect(url_for('views.posts_page'))

    return render_template('create_post.html', form=form)


@views.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post= Post.query.get_or_404(post_id)

    if post.owner_id != current_user.id:
        flash('You are not authorized to delete this post', category='error')
        return redirect(url_for('views.posts_page'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', category='success')
    return redirect(url_for('views.posts_page'))


@views.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.owner_id != current_user.id:
        flash('You are not authorized to delete this post', category='error')
        return redirect(url_for('views.posts_page'))
    
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        flash('Post Updated!', category='success')
        return redirect(url_for('views.posts_page'))
    
    return render_template('update_post.html', form=form)
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Post, User, Comment, Like
from . import db

front = Blueprint("front", __name__)

@front.route("/")
@front.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@front.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        data = request.form.get("text")

        if not data:
            flash('Post cannot be empty', category='error')
        else :
            post = Post(data=data, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created', category='success')
            return redirect(url_for('front.home'))

    return render_template("create_post.html", user=current_user)
    

@front.route("/delete-post/<int:id>")
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash('Post does not exist', category='error')
    elif current_user.id == post.author:
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted', category='success')
    return redirect(url_for('front.home'))


@front.route("/posts/<firstName>")
@login_required
def posts(firstName):
    user = User.query.filter_by(firstName=firstName).first()
    if user:
        posts = user.posts
        return render_template('posts.html', user=current_user, posts=posts, firstName=firstName)
    else :
        flash("No user with that username exists", category=error)
        return redirect(url_for('front.home'))


@front.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    data = request.form.get('data')

    if not data:
        flash('Comment cant be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(data=data, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exists', category='error')

    return redirect(url_for('front.home'))

@front.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id == comment.author:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('front.home'))

@front.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    post = Post.query.filter_by(id=post_id)

    if not post:
        flash('Post does not exist', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('front.home'))
from flask import render_template, redirect, url_for
from app.main import bp


@bp.route('/')
# home page
@bp.route('/home')
def home():
    user = 'Nicholas'
    return render_template('home.html', title='SankChewAir-E', user=user)


# about us page
@bp.route('/about')
def about():
    user = 'Nicholas'
    return render_template('about.html', title='SankChewAir-E', user=user)
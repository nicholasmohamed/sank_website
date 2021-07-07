import stripe
from flask import render_template, redirect, url_for
from app import db
from app.main import bp

page_list = [{"name": "PROGRAMS", "link": "main.programs"},
             {"name": "ABOUT", "link": "main.about"},
             {"name": "STORE", "link": "main.store"},
             {"name": "CONTACT", "link": "main.contact"}]

@bp.route('/')
# home page
@bp.route('/home')
def home():
    return render_template('home.html', title='SankChewAir-E', pages=page_list)


# about us page
@bp.route('/about')
def about():
    description = 'The aim of the Sankchewaire is to spread the ideals of hip-hop culture, encouraging unity, ' \
                  'selflessness and collective dedication. It is a haven for culture and like minded ' \
                  'people. We are a community that assists and inspires participants to achieve their aspirations' \
                  'through working collectively within hip hop culture, including gaming, dance and/or daily life.'

    return render_template('about.html', title='SankChewAir-E', description=description, pages=page_list)


# programs page
@bp.route('/programs')
def programs():
    description = 'The SankChewAir-E provides popping classes taught every Saturday by Freakwen-C, a member of the renowned' \
                  ' Moonrunners and Symbotic Monsters crews. To enroll, simply subscribe to the SankTtv twitch channel and' \
                  ' send us a message on our discord. Then you will have access to the class for as long as you are ' \
                  'subscribed.'

    return render_template('programs.html', title='SankChewAir-E', description=description, pages=page_list)


# store page
@bp.route('/store')
def store():
    description = 'Check out some of the SankChewAir-E swag.'

    # query items to sell in the store
    #items = db.query.all()
    return render_template('store.html', title='SankChewAir-E', description=description, pages=page_list)


# contact page
@bp.route('/contact')
def contact():
    links = {'instagram': {'link': 'https://www.instagram.com/sankchewaire_/', 'logo': 'assets/instagram_logo.svg'},
             'twitch': {'link': 'https://www.twitch.tv/sankttv', 'logo': 'assets/twitch_logo.svg'},
             'discord': {'link': 'https://discord.gg/ywVvEnkgjW', 'logo': 'assets/discord_logo.svg'},
             'youtube': {'link': 'https://www.youtube.com/SankTtv', 'logo': 'assets/youtube_logo.svg'}}
    return render_template('contact.html', title='SankChewAir-E', pages=page_list, links=links)
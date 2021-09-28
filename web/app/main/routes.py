import logging

# Flask imports
from flask import render_template, redirect, url_for, current_app
from flask_mail import Message
from app.main import bp
from app.models import SankMerch

logger = logging.getLogger('app_logger')

ABOUT = 0
SHOP = 1
CONTACT = 2


@bp.route('/')
# home page
@bp.route('/home')
def home():
    logger.info("Rendering homepage.")
    # all slides for the homepage carousel
    slides = [{'type': ABOUT, 'link': 'https://www.youtube.com/channel/UCgggw3qsvVx0_jVSkyGMSmw', 'img': 'assets/SANK_TV_LOGO.svg'},
              {'type': SHOP, 'link': 'https://www.twitch.tv/sankttv', 'img': 'assets/twitch_logo.svg'},
              {'type': CONTACT, 'link': 'https://discord.gg/ywVvEnkgjW', 'img': 'assets/discord_logo.svg'}]

    # query new arrivals from the shop for the shop carousel
    logger.info("Retrieving new arrivals")
    new_arrivals = SankMerch.query.all()

    return render_template('home.html', title='SankChewAir-E', pages=current_app.config['PAGE_LIST'], slides=slides,
                           new_arrivals=new_arrivals)


# about us page
@bp.route('/about')
def about():
    description = 'The aim of the Sankchewaire is to spread the ideals of hip-hop culture, encouraging unity, ' \
                  'selflessness and collective dedication. It is a haven for culture and like minded ' \
                  'people. We are a community that assists and inspires participants to achieve their aspirations' \
                  'through working collectively within hip hop culture, including gaming, dance and/or daily life.'

    return render_template('about.html', title='SankChewAir-E', description=description, pages=current_app.config['PAGE_LIST'])


# programs page
@bp.route('/programs')
def programs():
    description = 'The SankChewAir-E provides popping classes taught every Saturday by Freakwen-C, a member of the renowned' \
                  ' Moonrunners and Symbotic Monsters crews. To enroll, simply subscribe to the SankTtv twitch channel and' \
                  ' send us a message on our discord. Then you will have access to the class for as long as you are ' \
                  'subscribed.'

    return render_template('programs.html', title='SankChewAir-E', description=description, pages=current_app.config['PAGE_LIST'])


# contact page
@bp.route('/contact')
def contact():
    links = {'instagram': {'link': 'https://www.instagram.com/sankchewaire_/', 'logo': 'assets/instagram_logo.svg'},
             'twitch': {'link': 'https://www.twitch.tv/sankttv', 'logo': 'assets/twitch_logo.svg'},
             'discord': {'link': 'https://discord.gg/ywVvEnkgjW', 'logo': 'assets/discord_logo.svg'},
             'youtube': {'link': 'https://www.youtube.com/SankTtv', 'logo': 'assets/youtube_logo.svg'}}
    return render_template('contact.html', title='SankChewAir-E', pages=current_app.config['PAGE_LIST'], links=links)



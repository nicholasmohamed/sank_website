import logging

# Flask imports
from flask import render_template, redirect, url_for, current_app, request
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

    # query new arrivals from the shop for the shop carousel
    logger.info("Retrieving new arrivals")
    available_merch = SankMerch.query.all()

    about_text = "<b>SankChewAir-E</b> is an organization that is focused on creating and maintaining a community of artists " \
                 "from all social backgrounds to spread hip-hop culture through teaching, events and activities including dance," \
                 " video games and music.<br><br>We’re a community full of dancers," \
                 " gamers, artists and creators. But most of all, we’re a group of friends that want to spend good times " \
                 "with one another.<br><br>For more content, check out our YouTube channel: SankTV. Join our discord and " \
                 "connect with us on any or all of the social platforms listed below!" \
                 "<br><br><br>Contact us<br>info@sankchewaire.com"
    socials = [{'link': 'https://discord.gg/ywVvEnkgjW', 'logo': 'assets/discordIcon.svg'},
               {'link': 'https://www.youtube.com/channel/UCgggw3qsvVx0_jVSkyGMSmw', 'logo': 'assets/youtubeIcon.svg'},
               {'link': 'https://www.instagram.com/sankchewaire/', 'logo': 'assets/instagramIcon.svg'},
               {'link': 'https://www.facebook.com/SankChewAirE', 'logo': 'assets/facebookIcon.svg'},
               {'link': 'https://twitter.com/SankChewAirE_', 'logo': 'assets/twitterIcon.svg'}]
    logo = 'assets/Sank_Chew_Air_E_color_logo.svg'
    delivery_text = {"pickup": "Pick-up your order from 1-3390 Sherbrooke Street East, Montreal, QC. H1W 1C4",
                     "deliveryMtl": "You order will be delivered to you in Montreal at the earliest convenience "
                                    "after it is prepared. Delivery Fee: $3.00",
                     "deliveryCan": "You order will be delivered to you by standard shipping after it is prepared "
                                    "Delivery Fee: $12.00"}
    domain = current_app.config['YOUR_DOMAIN']

    # determine which version of site to use: mobile or desktop
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    if "iphone" in user_agent:
        webpage = 'mobile_home.html'
        sidebar_width = '700px'
    elif "android" in user_agent:
        webpage = "mobile_home.html"
        sidebar_width = '700px'
    else:
        webpage = 'home.html'
        sidebar_width = '400px'

    return render_template(webpage, title='SankChewAir-E', domain=domain, about_text=about_text,
                           logo=logo, available_merch=available_merch, socials=socials,
                           delivery_text=delivery_text, sidebar_width=sidebar_width)


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


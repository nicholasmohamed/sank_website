import logging

# Flask imports
from flask import render_template, redirect, url_for, current_app, request
from flask_mail import Message
from app.main import bp, Blueprint
from app.models import SankMerch

logger = logging.getLogger('app_logger')

ABOUT = 0
SHOP = 1
CONTACT = 2


# Add in variables used across all pages (base.html)
@bp.app_context_processor
def inject_sidebar_width():
    # determine which version of site to use: mobile or desktop
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    if "iphone" in user_agent:
        sidebar_width = '700px'
    elif "android" in user_agent:
        sidebar_width = '700px'
    else:
        sidebar_width = '400px'
    return dict(sidebar_width=sidebar_width)


@bp.app_context_processor
def inject_available_merch():
    # query new arrivals from the shop for the shop carousel
    logger.info("Retrieving new arrivals")
    available_merch = SankMerch.query.all()
    return dict(available_merch=available_merch)


@bp.app_context_processor
def inject_delivery_text():
    delivery_text = {"pickup": "Pick-up your order from 1-3390 Sherbrooke Street East, Montreal, QC. H1W 1C4",
                     "deliveryMtl": "You order will be delivered to you in Montreal at the earliest convenience "
                                    "after it is prepared.<br><br>Delivery Fee: $3.00",
                     "deliveryCan": "You order will be delivered to you by standard shipping after it is prepared "
                                    "<br><br>Delivery Fee: $12.00"}
    return dict(delivery_text=delivery_text)


@bp.app_context_processor
def inject_domain():
    domain = current_app.config['YOUR_DOMAIN']
    return dict(domain=domain)


@bp.app_context_processor
def inject_pages():
    pages = current_app.config['PAGE_LIST']
    return dict(pages=pages)


@bp.route('/')
# home page
@bp.route('/home')
def home():
    logger.info("Rendering homepage.")

    about_text = "<b>SankChewAir-E</b> is an organization that is focused on creating and maintaining a community of artists " \
                 "from all social backgrounds to spread hip-hop culture through teaching, events and activities including dance," \
                 " video games, fashion and music.<br><br>We’re a community full of dancers," \
                 " gamers, artists and creators. But most of all, we’re a group of friends that want to spend good times " \
                 "with one another.<br><br>For more content, check out our YouTube channel: SankTV. Join our discord and " \
                 "connect with us on any or all of the social platforms listed below!" \
                 "<br><br><br>Contact us<br>info@sankchewaire.com"
    home_text = "<b class=\"sankStyledText\">SankChewAir-E</b> is an organization that is focused on creating and maintaining a community of artists " \
                 "from all social backgrounds to spread hip-hop culture through teaching, events and activities including dance," \
                 " video games, fashion and music.<br><br>We’re a community full of dancers," \
                 " gamers, artists and creators. But most of all, we’re a group of friends that want to spend good times " \
                 "with one another."
    socials = [{'link': 'https://discord.gg/ywVvEnkgjW', 'logo': 'assets/discordIcon.svg'},
               {'link': 'https://www.youtube.com/channel/UCgggw3qsvVx0_jVSkyGMSmw', 'logo': 'assets/youtubeIcon.svg'},
               {'link': 'https://www.instagram.com/sankchewaire/', 'logo': 'assets/instagramIcon.svg'},
               {'link': 'https://www.facebook.com/SankChewAirE', 'logo': 'assets/facebookIcon.svg'},
               {'link': 'https://twitter.com/SankChewAirE', 'logo': 'assets/twitterIcon.svg'}]
    logo = 'assets/Sank_Chew_Air_E_color_logo.svg'

    # determine which version of site to use: mobile or desktop
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    if "iphone" in user_agent:
        webpage = 'mobile_home.html'
    elif "android" in user_agent:
        webpage = "mobile_home.html"
    else:
        webpage = 'home.html'

    return render_template(webpage, title='SankChewAir-E', about_text=about_text,
                           logo=logo, socials=socials, home_text=home_text)


# about us page
@bp.route('/about')
def about():
    mission_text = 'The aim of the SankChewAir-E is to spread the ideals of hip-hop culture, encouraging unity, ' \
                    'selflessness and collective dedication. It is a haven for culture and like minded ' \
                    'people. SankChewAir-E is an organization that is focused on creating and maintaining a community' \
                    ' of artists from all social backgrounds to spread hip-hop culture through teaching, events and ' \
                    'activities including dance, video games, fashion and music <br><br>We’re a community full of dancers,' \
                    ' gamers, artists and creators. But most of all, we’re a group of friends that want to spend good times ' \
                    'with one another.<br><br>For more content, check out our YouTube channel: SankTV. Join our discord and '\
                    'connect with us on any or all of the social platforms listed below!' \
                    '<br><br><br>Contact us<br>info@sankchewaire.com'
    rep_the_sank_text = ""
    our_story_text = ""
    socials = [{'link': 'https://discord.gg/ywVvEnkgjW', 'logo': 'assets/discordIcon.svg'},
               {'link': 'https://www.youtube.com/channel/UCgggw3qsvVx0_jVSkyGMSmw', 'logo': 'assets/youtubeIcon.svg'},
               {'link': 'https://www.instagram.com/sankchewaire/', 'logo': 'assets/instagramIcon.svg'},
               {'link': 'https://www.facebook.com/SankChewAirE', 'logo': 'assets/facebookIcon.svg'},
               {'link': 'https://twitter.com/SankChewAirE_', 'logo': 'assets/twitterIcon.svg'}]

    return render_template('about.html', title='SankChewAir-E', mission_text=mission_text, socials=socials,
                           rep_the_sank_text=rep_the_sank_text, our_story_text=our_story_text)


# programs page
@bp.route('/programs')
def programs():
    description = 'The SankChewAir-E provides popping classes taught every Saturday by Freakwen-C, a member of the renowned' \
                  ' Moonrunners and Symbotic Monsters crews. To enroll, simply subscribe to the SankTtv twitch channel and' \
                  ' send us a message on our discord. Then you will have access to the class for as long as you are ' \
                  'subscribed.'

    return render_template('programs.html', title='SankChewAir-E', description=description)


# contact us page
@bp.route('/contact')
def contact():
    return 3
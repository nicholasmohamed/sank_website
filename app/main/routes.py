import logging
import csv

# Flask imports
from flask import render_template, redirect, url_for, current_app, request, send_from_directory
from flask_mail import Message
from app.main import bp, Blueprint
from app.models import SankMerch

logger = logging.getLogger('app_logger')

ABOUT = 0
SHOP = 1
CONTACT = 2

ABOUT_ROWS = 3


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


@bp.app_context_processor
def inject_site_dictionary():
    site_dictionary = parse_tsv_file(bp.static_folder + '\\lang\\english_text.tsv')
    return dict(site_text=site_dictionary)


@bp.route('/')
# home page
@bp.route('/home')
def home():
    logger.info("Rendering homepage.")

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

    return render_template(webpage, title='SankChewAir-E', logo=logo)


# about us page
@bp.route('/about')
def about():
    socials = [{'link': 'https://discord.gg/ywVvEnkgjW', 'logo': 'assets/discordIcon.svg'},
               {'link': 'https://www.youtube.com/channel/UCgggw3qsvVx0_jVSkyGMSmw', 'logo': 'assets/youtubeIcon.svg'},
               {'link': 'https://www.instagram.com/sankchewaire/', 'logo': 'assets/instagramIcon.svg'},
               {'link': 'https://www.facebook.com/SankChewAirE', 'logo': 'assets/facebookIcon.svg'},
               {'link': 'https://twitter.com/SankChewAirE_', 'logo': 'assets/twitterIcon.svg'}]

    return render_template('about.html', title='SankChewAir-E', socials=socials)


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


# parses tsv file to create dictionary of all text on website
def parse_tsv_file(filename):
    logger.info("parse_tsv_file: parsing tsv file.")
    language_dictionary = {}
    pages = ['about', 'home']

    # initialize all pages
    for page in pages:
        language_dictionary[page] = {}

    with open(filename) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t", quotechar="\'", escapechar='\\')
        for row, line in enumerate(tsvreader):
            i = 1
            # do not parse title row
            if row > 0:
                # set keys based on the row (ie. first x rows are for the about section, next y rows for landing)
                if 0 < row < ABOUT_ROWS + 1:
                    page = pages[0]
                    keys = ['title', 'text']
                else:
                    page = pages[1]
                    keys = ['slogan_text', 'text']
                # for every key, record value listed in tsv
                dict = {}
                for key in keys:
                    dict[key] = line[i].replace("â€™", "\'")
                    i += 1
                # add line to the corresponding page
                language_dictionary[page][line[0]] = dict

    # For use in debugging
    # print(language_dictionary)

    logger.info("parse_tsv_file: tsv parsed successfully.")
    return language_dictionary

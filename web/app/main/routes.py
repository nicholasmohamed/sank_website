# Stripe imports
import stripe
import sys
import os
import json
import logging

# Flask imports
from flask import render_template, redirect, url_for, current_app, jsonify, request
from flask_mail import Message
from app import db, mail
from app.main import bp

logger = logging.getLogger('app_logger')

page_list = [{"name": "PROGRAMS", "link": "main.programs"},
             {"name": "ABOUT", "link": "main.about"},
             {"name": "STORE", "link": "main.store"},
             {"name": "CONTACT", "link": "main.contact"}]


@bp.route('/')
# home page
@bp.route('/home')
def home():
    logger.info("Rendering homepage.")
    slides = [{'link': 'https://www.youtube.com/channel/UCgggw3qsvVx0_jVSkyGMSmw', 'img': 'assets/SANK_TV_LOGO.svg'},
              {'link': 'https://www.twitch.tv/sankttv', 'img': 'assets/twitch_logo.svg'},
              {'link': 'https://discord.gg/ywVvEnkgjW', 'img': 'assets/discord_logo.svg'}]
    return render_template('home.html', title='SankChewAir-E', pages=page_list, slides=slides)


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
    items = {}
    return render_template('store.html', title='SankChewAir-E', description=description, items=items, pages=page_list)


# contact page
@bp.route('/contact')
def contact():
    links = {'instagram': {'link': 'https://www.instagram.com/sankchewaire_/', 'logo': 'assets/instagram_logo.svg'},
             'twitch': {'link': 'https://www.twitch.tv/sankttv', 'logo': 'assets/twitch_logo.svg'},
             'discord': {'link': 'https://discord.gg/ywVvEnkgjW', 'logo': 'assets/discord_logo.svg'},
             'youtube': {'link': 'https://www.youtube.com/SankTtv', 'logo': 'assets/youtube_logo.svg'}}
    return render_template('contact.html', title='SankChewAir-E', pages=page_list, links=links)


# Create stripe checkout page
@bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    stripe.api_key = current_app.config['STRIPE_API_KEY']

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'cad',
                        'unit_amount': 60,
                        'product_data': {
                            'name': 'T-shirt',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'adjustable_quantity': {
                        'enabled': True,
                        'minimum': 1,
                        'maximum': 10,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=current_app.config['YOUR_DOMAIN'] + '/store',
            cancel_url=current_app.config['YOUR_DOMAIN'] + '/store'
        )
        return redirect(checkout_session.url, code=303)
    except:
        # TODO handle errors
        logger.error("Unexpected error:", sys.exc_info()[0])
        return redirect(current_app.config['YOUR_DOMAIN'] + '/home.html')


# webhook to handle payment responses
@bp.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    try:
        event = json.loads(payload)
    except:
        logger.error('⚠️  Webhook error while parsing basic request.')
        return jsonify(success=False)

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        logger.info('Payment for {} succeeded'.format(payment_intent['amount']))
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
        handle_order(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        logger.error('Unhandled event type {}'.format(event['type']))
    return jsonify(success=True)


# save into database and send customer a receipt
def handle_order(session):
    recipient_email = session['charges']['data'][0]['billing_details']['email']
    logger.info('Sending e-mail to ' + recipient_email)
    msg = Message('Thank you for your purchase! We have attached your receipt.', sender=current_app.config['MAIL_USERNAME'],
                  recipients=[recipient_email])
    msg.body = "SankChewAir-E Order Confirmation"
    mail.send(msg)
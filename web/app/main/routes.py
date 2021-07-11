# Stripe imports
import stripe
import sys

# Flask imports
from flask import render_template, redirect, url_for
from app import db
from app.main import bp

# Using Django
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

page_list = [{"name": "PROGRAMS", "link": "main.programs"},
             {"name": "ABOUT", "link": "main.about"},
             {"name": "STORE", "link": "main.store"},
             {"name": "CONTACT", "link": "main.contact"}]

YOUR_DOMAIN = 'http://127.0.0.1:5000'
stripe.api_key = 'sk_test_51J9ZCCBUeaWrljhjmzDSI7l72P1dbtRAW5Ro9griA0xs4Ymg3DmeDahi7M29njUANK1AYUvuAp0PxXWtapDDRgam00gzLucYR0'
endpoint_secret = 'whsec_RnZjMuCPxRLGnDxIMboPeDjgSerA2Dp0'


@bp.route('/')
# home page
@bp.route('/home')
def home():
    slides = [{'link': 'https://www.youtube.com/channel/UCgggw3qsvVx0_jVSkyGMSmw', 'img': 'assets/SANK_TV_LOGO.svg'},
              {'link': 'https://www.twitch.tv/sankttv', 'img': 'assets/twitch_logo.svg'},
              {'link': 'https://discord.gg/ywVvEnkgjW', 'img': 'assets/discord_logo.svg'},
              {'link': 'https://www.youtube.com/SankTtv', 'img': 'assets/youtube_logo.svg'}]
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
            success_url=YOUR_DOMAIN + '/store',
            cancel_url=YOUR_DOMAIN + '/store'
        )
        return redirect(checkout_session.url, code=303)
    except:
        # TODO handle errors
        print("Unexpected error:", sys.exc_info()[0])
        return redirect(YOUR_DOMAIN + '/home.html')


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # handle purchase...
        handle_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


# save into database and send customer a receipt
def handle_order(session):
    # TODO: fill me in
    print("Handling order")
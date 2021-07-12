# Stripe imports
import stripe
import sys
import os
import json
import logging

from flask import render_template, redirect, url_for, current_app, jsonify, request
from flask_mail import Message
from app import db, mail
from app.store import bp
from app.models import SankMerch

logger = logging.getLogger('app_logger')


# TODO adding and removing items from database
@bp.route('/database')
def database():
    items = SankMerch.query.all()
    if not items:
        items = {}
    return render_template('store/database.html', title='SankChewAir-E', items=items)


# store page
@bp.route('/store')
def store():
    description = 'Check out some of the SankChewAir-E swag.'

    # query items to sell in the store
    items = SankMerch.query.all()
    if not items:
        items = {}
    return render_template('store/store.html', title='SankChewAir-E', description=description, items=items,
                           pages=current_app.config['PAGE_LIST'])


@bp.route('/stripe-config')
def stripe_config():
    config = {'publicKey': current_app.config['STRIPE_API_PUBLIC_KEY']}
    return jsonify(config)


# Create stripe checkout page
@bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    stripe.api_key = current_app.config['STRIPE_API_SECRET_KEY']

    try:
        data = json.loads(request.data)

        print(data)
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
        return jsonify({'sessionId': checkout_session['id']})
    except:
        # TODO handle errors
        logger.error("Unexpected error:", sys.exc_info()[0])
        return redirect(current_app.config['YOUR_DOMAIN'] + '/home')


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
        # handle the successful payment intent.
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
    msg = Message('SankChewAir-E Order Confirmation', sender=current_app.config['MAIL_USERNAME'],
                  recipients=[recipient_email])
    msg.body = 'Thank you for your purchase! We have attached your receipt.'
    mail.send(msg)


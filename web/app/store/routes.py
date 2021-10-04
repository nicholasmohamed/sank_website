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
    return render_template('store/database.html', title='SankChewAir-E', items=items, length=len(items))


@bp.route('/update-database', methods=['POST', 'GET'])
def update_database():
    if request.method == 'POST':
        logger.info("Updating database")
        result = request.form

        item_list = parse_returned_values(result)
        update_database_items(item_list)

        return redirect("/database")


def update_database_items(item_list):
    database_items = SankMerch.query.all()
    for client_item in item_list:
        # get item from database that corresponds to item returned from client
        try:
            # check for id in database items
            database_item = next(item for item in database_items if int(item.id) == int(client_item['id']))

            # check if needed to delete
            if 'remove' in client_item:
                db.session.delete(database_item)
                db.session.commit()
            else:
                # update the item with new values
                database_item.id = client_item.get('id')
                database_item.name = client_item.get('name')
                database_item.price = client_item.get('price')
                database_item.description = client_item.get('description')
                database_item.imageLink = client_item.get('imageLink')
                database_item.quantity = client_item.get('quantity')
                database_item.isAvailable = client_item.get('isAvailable')
                database_item.tags = client_item.get('tags')

                # add items to database
                db.session.commit()
        except StopIteration:
            # create new item
            database_item = SankMerch(id=client_item.get('id'), name=client_item.get('name'), price=client_item.get('price'),
                                      imageLink=client_item.get('imageLink'),description=client_item.get('description'),
                                      quantity=client_item.get('quantity'), isAvailable=client_item.get('isAvailable'),
                                      tags=client_item.get('tags'))
            db.session.add(database_item)
            db.session.commit()


# Returns all items in a usable format (python dictionary)
def parse_returned_values(items):
    length = len(items.getlist('id'))
    item_list = []

    for i in range(length):
        item = {'id': items.getlist('id')[i], 'name': items.getlist('name')[i], 'price': items.getlist('price')[i],
                'imageLink': items.getlist('imageLink')[i], 'description': items.getlist('description')[i],
                'quantity': items.getlist('quantity')[i],
                'isAvailable': items.getlist('isAvailable')[i].lower() in ['True', 'true', 't', 'T']}
        # check for removal
        if i < len(items.getlist('remove')):
            if items.getlist('remove')[i] in ['True', 'true', 't', 'T']:
                item['remove'] = True

        item_list.append(item)
    return item_list


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
    logger.info('Creating checkout session')
    stripe.api_key = current_app.config['STRIPE_API_SECRET_KEY']

    try:
        # retrieve data passed to checkout
        data = json.loads(request.data)

        # convert data to item array
        items = []
        for item in data:
            merch = SankMerch.query.get(item['id'])
            if merch:
                items.append(convert_database_to_cart_item(merch, item))

        merch_items = generate_line_items(items)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=merch_items,
            mode='payment',
            success_url=current_app.config['YOUR_DOMAIN'] + '/store',
            cancel_url=current_app.config['YOUR_DOMAIN'] + '/store'
        )

        return jsonify({'sessionId': checkout_session['id']})
    except:
        # TODO handle errors
        logger.error("Unexpected error:", sys.exc_info()[0])
        return redirect(current_app.config['YOUR_DOMAIN'] + '/home')


# TODO make more efficient
# take database information and cart information and produce line item
def convert_database_to_cart_item(merch, data):
    item = {}
    item['price'] = merch.price
    item['quantity'] = data['quantity']
    item['name'] = merch.name
    # item['imageLink'] = merch.imageLink
    return item


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


# create line items for checkout
def generate_line_items(items):
    line_items = []

    # TODO handle image links
    # url_for("static", filename=item.imageLink)

    for item in items:
        line_item = {
            'price_data': {
                'currency': 'cad',
                'unit_amount': item['price'] * 10,
                'product_data': {
                    'name': item['name'],
                    'images': [],
                },
            },
            'adjustable_quantity': {
                'enabled': True,
                'minimum': 1,
                'maximum': 10,
            },
            'quantity': item['quantity'],
        }
        line_items.append(line_item)
    return line_items

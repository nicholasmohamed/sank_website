# Stripe imports
import stripe
import sys
import os
import json
import logging

from flask import render_template, redirect, url_for, current_app, jsonify, request
from flask_mail import Message
from app import db, mail
from app.store import bp, Blueprint
from app.models import SankMerch, Size, Order, Image
from app.models import PurchasedMerch as pm

logger = logging.getLogger('app_logger')

pending_orders = {}


@bp.route('/shop')
def shop():
    logger.info("Rendering shop.")

    return render_template('store/shop.html', title='SankChewAir-E')


@bp.route('/database')
def database():
    items = SankMerch.query.all()
    if not items:
        items = {}
    return render_template('store/database.html', title='SankChewAir-E', domain=current_app.config['YOUR_DOMAIN'],
                           items=items)


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
                item_sizes = Size.query.filter_by(merch_id=database_item.id).all()
                db.session.delete(database_item)
                for item_size in item_sizes:
                    db.session.delete(item_size)
                db.session.commit()
            else:
                # update the item with new values
                database_item.id = client_item.get('id')
                database_item.name = client_item.get('name')
                database_item.price = client_item.get('price')
                database_item.description = client_item.get('description')
                database_item.long_description = client_item.get('long_description')
                database_item.manufacturing_description = client_item.get('mfg_description')
                database_item.care_instructions = client_item.get('care_instructions')
                database_item.quantity = client_item.get('quantity')
                database_item.isAvailable = client_item.get('isAvailable')
                database_item.tags = client_item.get('tags')

                # handle image table (separate related database)
                item_images = Image.query.filter_by(merch_id=database_item.id).all()

                # handle size table (separate related database)
                item_sizes = Size.query.filter_by(merch_id=database_item.id).all()

                update_related_table('sizes', item_sizes, client_item, database_item)

                update_related_table('imageLink', item_images, client_item, database_item)

        except StopIteration:
            # create new item
            database_item = SankMerch(id=client_item.get('id'), name=client_item.get('name'), price=client_item.get('price'),
                                      description=client_item.get('description'), quantity=client_item.get('quantity'),
                                      isAvailable=client_item.get('isAvailable'), tags=client_item.get('tags'))
            db.session.add(database_item)

        # add items to database
        db.session.commit()

        logger.info("Database updated.")


# updates related array table for sank_merch
def update_related_table(table_name, item_properties, client_item, database_item):
    # first check if there are changes
    # then if there is same number in db, replace data. If not, replace everything
    if len(client_item.get(table_name)) > 0:
        if client_item.get(table_name)[0] != '':
            if len(item_properties) != len(client_item.get(table_name)):
                logger.info("Rewriting all " + table_name + " for merch_id: " + database_item.id)
                for item_property in item_properties:
                    db.session.delete(item_property)
                for i, property in enumerate(client_item.get(table_name)):
                    if table_name == "sizes":
                        db.session.add(Size(size=property, merch_id=database_item.id))
                    elif table_name == "imageLink":
                        db.session.add(Image(imageLink=property, merch_id=database_item.id))
            else:
                logger.info("Changing existing " + table_name + " for merch_id: " + database_item.id)
                for i, property in enumerate(client_item.get(table_name)):
                    if table_name == "sizes":
                        item_properties[i].size = property
                    elif table_name == "imageLink":
                        item_properties[i].imageLink = property


# Returns all items in a usable format (python dictionary)
def parse_returned_values(items):
    logger.info("Parsing values.")
    length = len(items.getlist('id'))
    item_list = []

    for i in range(length):
        sizes = parse_returned_array_property(items, 'sizes', i)
        images = parse_returned_array_property(items, 'imageLink', i)

        item = {'id': items.getlist('id')[i], 'name': items.getlist('name')[i], 'price': items.getlist('price')[i],
                'imageLink': images, 'description': items.getlist('description')[i],
                'sizes': sizes, 'quantity': items.getlist('quantity')[i],
                'long_description': items.getlist('long_description')[i],
                'mfg_description': items.getlist('mfg_description')[i],
                'care_instructions': items.getlist('care_instructions')[i],
                'isAvailable': items.getlist('isAvailable')[i].lower() in ['True', 'true', 't', 'T']}

        logger.info(item)
        # check for removal
        if i < len(items.getlist('remove')):
            if items.getlist('remove')[i] in ['True', 'true', 't', 'T']:
                item['remove'] = True

        item_list.append(item)
    return item_list


# parse array property
def parse_returned_array_property(items, item_name, index):
    logger.info(len(items.getlist(item_name)))
    if index < len(items.getlist(item_name)):
        properties = items.getlist(item_name)[index].split(",")
        # remove leading white-spaces
        for x, property in enumerate(properties):
            properties[x] = property.lstrip(' ')
    else:
        properties = []

    return properties


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
        for item in data['cart']:
            merch = SankMerch.query.get(item['id'])
            if merch:
                items.append(convert_database_to_cart_item(merch, item))

        merch_items = generate_line_items(items)

        # Determine shipping rate 1 - Delivery MTl, 2- Delivery CAN
        if int(data['shipping']) == 1:
            shipping_rate = current_app.config['STRIPE_SHIPPING_RATE_1']
        elif int(data['shipping']) == 2:
            shipping_rate = current_app.config['STRIPE_SHIPPING_RATE_2']
        else:
            shipping_rate = ""

        if shipping_rate != "":
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                shipping_rates=[shipping_rate],
                shipping_address_collection={
                    'allowed_countries': ['CA'],
                },
                line_items=merch_items,
                mode='payment',
                success_url=current_app.config['YOUR_DOMAIN'],
                cancel_url=current_app.config['YOUR_DOMAIN']
            )
        else:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=merch_items,
                mode='payment',
                success_url=current_app.config['YOUR_DOMAIN'],
                cancel_url=current_app.config['YOUR_DOMAIN']
            )
        logger.info('Checkout session created')

        pending_orders[checkout_session['payment_intent']] = {"line_items": items}
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
    item['quantity'] = data.get('quantity')
    item['name'] = merch.name
    item['size'] = Size.query.filter_by(merch_id=merch.id, size=data.get('size')).first()
    item['variation'] = data.get('variation')
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
def handle_order(payment_intent):
    recipient_email = payment_intent['charges']['data'][0]['billing_details']['email']
    source_email = "info@sankchewaire.com"

    # get line items
    items = pending_orders[payment_intent['id']]['line_items']

    # format string for list of items
    item_string = "\n"
    for line_item in items:
        item_string += "\n" + str(line_item['name']) + "\t\t" + str(line_item['price']) + "\n"

    # send e-mail
    logger.info('Sending e-mail to ' + recipient_email)
    msg = Message('SankChewAir-E Order Confirmation', sender=current_app.config['MAIL_USERNAME'],
                  recipients=[recipient_email, source_email])
    msg.body = 'Thank you for your purchase! We have attached your receipt.' + item_string
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
                'unit_amount_decimal': item['price'] * 100,
                'product_data': {
                    'name': item['name'],
                    'images': [],
                },
            },
            'tax_rates': [current_app.config['STRIPE_PROVINCIAL_TAX'], current_app.config['STRIPE_FEDERAL_TAX']],
            'quantity': item['quantity'],
        }
        line_items.append(line_item)
    return line_items


# create order object based on checkout items
def construct_order(items):
    order = Order(status="In Progress")
    db.session.add(order)
    for item in items:
        purchased_item = pm(merch_id=item.id, size_id=item.size, order_id=order.id)
        db.session.add(purchased_item)
    db.session.commit()
    return order.id

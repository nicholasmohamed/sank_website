import sys
import os
import json
import logging

from flask import render_template, redirect, url_for, current_app, jsonify, request, g
from requests.exceptions import HTTPError
from app import mail, User
from app.foamwars import bp, Blueprint
from app.database import db_session
from app.common import *

import firebase_admin
from firebase_admin import credentials, messaging
firebase_cred = credentials.Certificate('firebase-admin.json')
firebase_app = firebase_admin.initialize_app(firebase_cred)

logger = logging.getLogger('app_logger')

# webhook to handle payment responses
@bp.route('/challenge_request', methods=['POST'])
def challenge_request():
    payload = request.data

    data = json.loads(payload)
    send_token_push(data['notification']['title'], data['notification']['body'], data['token'])

    logger.info("Received data. Sending challenge request...")
    try:
        data = json.loads(payload)
        logger.info("Parsed. Correctly.")

        send_token_push(data['notification']['title'], data['notification']['body'], data['token'])
    except HTTPError as e:
        print(e.response.text)
    except:
        logger.error('⚠️  Webhook error while parsing basic request.')
        return jsonify(success=False)
    return jsonify(success=True)


def send_token_push(title, body, tokens): 
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,   
            body=body
        ), 
        tokens=tokens
    ) 
    messaging.send_multicast(message)
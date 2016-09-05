#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Feedbackbot - slack bot for providing teammates with anonymous feedback.
"""

import argparse
import os
import re
import sys
from slacker import Slacker


DESCRIPTION = 'Procedure to provide teammates with anonymous feedback on slack'

USER_NOT_FOUND = 'USER_NOT_FOUND'
COULD_NOT_FIND_CHANNEL = 'COULD_NOT_FIND_CHANNEL'

FEEDBACK_REGEX = r"""
^tell\s             # 'tell' at the start of the string
(?P<username>\S*)\s # group any non-whitespace as username
(?P<feedback>.*$)   # grab any following characters until EOS as feedback
"""
FEEDBACK_STRING = 'An anonymous user wanted to tell you: "{}"'


def list_im_channels(client):
    """Returns the ids of the channels the user is participating in.
    """
    r = client.im.list()
    return [c for c in r.body.get('ims')] if r.successful else []


def list_text_from_channel(client, channel_id, oldest=0):
    """Create a list of the individual messages in a channel.
    """
    r = client.im.history(channel=channel_id, oldest=oldest)
    return [m.get('text') for m in r.body.get('messages')] \
        if r.successful else []


def open_im(client, user_id):
    r = client.im.open(user=user_id)
    return r.successful


def post_message(client, channel_id, text):
    r = client.chat.post_message(
        channel=channel_id,
        text=FEEDBACK_STRING.format(text),
        as_user=True)
    return r.successful


def get_feedback_ims(client):
    feedback_messages = []
    for c in list_im_channels(client):
        channel_text = list_text_from_channel(client, c.get('id'))
        for t in channel_text:
            message = process_feedback(t)
            if message:
                feedback_messages.append(message)
    return feedback_messages


def list_users(client):
    r = client.users.list()
    return r.body.get('members') if r.successful else []


def get_im_channel_id(client, user_id):
    channels = list_im_channels(client)
    for c in channels:
        if user_id == c.get('user'):
            channel_id = c.get('id')
            break
    else:
        channel_id = COULD_NOT_FIND_CHANNEL
    return channel_id


def get_user_id(client, username):
    users = list_users(client)

    for user in users:
        if username == user.get('name'):
            user_id = user.get('id')
            break
    else:
        user_id = USER_NOT_FOUND
    return user_id


def process_feedback(feedback_string):
    m = re.search(FEEDBACK_REGEX, feedback_string, re.VERBOSE)
    return {'username': m.group('username'), 'feedback': m.group('feedback')} \
        if m is not None else {}


def send_feedback(client, user_id, feedback):
    open_im(client, user_id)
    channel_id = get_im_channel_id(client, user_id)
    post_message(client, channel_id, feedback)


def process(client):
    messages = get_feedback_ims(client)
    for m in messages:
        user_id = get_user_id(client, m.get('username'))
        send_feedback(client, user_id, m.get('feedback'))
    return


def get_token(parser):
    results = parser.parse_args()
    try:
        token = results.token
    except(AttributeError):
        pass
    try:
        token = os.environ['SLACK_TOKEN']
    except(KeyError):
        pass
    if not isinstance(token, str) or token is None:
        raise Exception('No token found for Slack API.')
    return token


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--token', action='store', dest='token')
    token = get_token(parser)

    client = Slacker(token)

    process(client)


if __name__ == "__main__":
    sys.exit(main())

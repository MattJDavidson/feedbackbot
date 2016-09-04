# -*- coding: utf-8 -*-
"""
Tests for `feedbackbot` module.
"""
import pytest
from feedbackbot.feedbackbot import (get_user_id,
                                     list_im_channels,
                                     list_text_from_channel,
                                     list_users,
                                     post_message,
                                     process_feedback,
                                     USER_NOT_FOUND)
from slackclient import SlackClient

TOKEN = 'xoxb-70925999889-TqRmuQhNHjo479zlxVbkIJn3'
CHANNEL_ID = 'D22SU1KEG'


@pytest.fixture
def client():
    return SlackClient(TOKEN)


def test_get_user_id(client):
    r = get_user_id(client, '_')
    assert r == USER_NOT_FOUND


def test_list_users(client):
    r = list_users(client)
    assert r is not None


def test_list_im_channels(client):
    r = list_im_channels(client)
    assert isinstance(r, list)


def test_list_text_from_channel(client):
    r = list_text_from_channel(client, '_')
    assert r is not None


def test_post_message_channel_exists(client):
    r = post_message(client, CHANNEL_ID, 'basic message test')
    assert r


def test_post_message_channel_doesnt_exist(client):
    r = post_message(client, '_', '_')
    assert not r


def test_process_feedback():
    f = 'tell my_family I love them'
    feedback = process_feedback(f)
    assert 'my_family' == feedback.get('username')
    assert 'I love them' == feedback.get('feedback')


def test_process_unparseable_feedback():
    assert {} == process_feedback('_')

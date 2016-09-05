# -*- coding: utf-8 -*-
"""
Tests for `feedbackbot` module.
"""
import mock
import pytest
from feedbackbot.feedbackbot import (get_user_id,
                                     list_im_channels,
                                     list_text_from_channel,
                                     list_users,
                                     post_message,
                                     process_feedback,
                                     USER_NOT_FOUND)

NAME = 'name'
ID = 'id'


@pytest.fixture
def client():
    return mock.MagicMock()


@mock.patch('feedbackbot.feedbackbot.list_users')
def test_get_user_id_no_user(list_users, client):
    list_users.return_value = []
    r = get_user_id(client, '_')
    assert r == USER_NOT_FOUND


@mock.patch('feedbackbot.feedbackbot.list_users')
def test_get_user_id_user_found(list_users, client):
    list_users.return_value = [{'name': NAME, 'id': ID}]
    id = get_user_id(client, NAME)
    assert id == ID


def test_list_users(client):
    client.users.list.return_value.body = {'members': ['_']}
    r = list_users(client)
    assert r == ['_']


def test_list_users_unsuccessful(client):
    client.users.list.return_value.successful = False
    r = list_users(client)
    assert r == []


def test_list_im_channels(client):
    client.im.list.return_value.body = {'ims': ['_']}
    r = list_im_channels(client)
    assert r == ['_']


def test_list_im_channels_unsuccessful(client):
    client.im.list.return_value.successful = False
    r = list_im_channels(client)
    assert r == []


def test_list_text_from_channel(client):
    client.im.history.return_value.body = {'messages': [{'text': '_'}]}
    r = list_text_from_channel(client, '_')
    assert r == ['_']


def test_list_text_from_channel_unsuccessful(client):
    client.im.history.return_value.successful = False
    r = list_text_from_channel(client, '_')
    assert r == []


def test_post_message_channel_exists(client):
    client.chat.post_message.return_value.successful = True
    r = post_message(client, '_', '_')
    assert r


def test_post_message_channel_doesnt_exist(client):
    client.chat.post_message.return_value.successful = False
    r = post_message(client, '_', '_')
    assert not r


@mock.patch('feedbackbot.feedbackbot.re.search')
def test_process_feedback(search):
    m = mock.Mock()
    m.group.return_value = '_'
    search.return_value = m

    feedback = process_feedback('_')
    assert '_' == feedback.get('username')
    assert '_' == feedback.get('feedback')


@mock.patch('feedbackbot.feedbackbot.re.search')
def test_process_unparseable_feedback(search):
    search.return_value = None
    assert {} == process_feedback('_')

#!/usr/bin/python

import logging
from flotype.bridge import Bridge 

bridge = Bridge(log=5, api_key='abcdefgh')

class MsgHandler(object):
    def msg(self, name, message):
        print(name + ': ' + message)

class LobbyHandler(object):
    def __init__(self, name):
        self.name = name
        self.lobby = None

    def __call__(self, channel, name):
        self.lobby = channel
        self.send('Hello, world.')

    def send(self, message):
        self.lobby.msg(self.name, message)

def start_client():
    lobby = LobbyHandler('Vedant')
    chat = bridge.get_service('chatty')
    chat.join('lobby', MsgHandler(), lobby)

bridge.ready(start_client)
bridge.connect()

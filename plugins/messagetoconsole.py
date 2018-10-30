from util import Events
import discord
import re

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.Message("consoleprint")]

    async def handle_message(self, message_object):
        #prints incoming messages to console, as I felt this would be pretty useful when testing various commands. This is more of a debugging feature. 
        print('[' + str(message_object.server.name) + '][#' + str(message_object.channel) + '][' + str(message_object.author) + '][' + str(message_object.content) + ']')
